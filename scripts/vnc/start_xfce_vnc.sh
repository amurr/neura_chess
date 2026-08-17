#!/usr/bin/env bash
# Run on the pod. Starts XFCE on TigerVNC display :1, bound to 127.0.0.1 only.
# Do not expose 5901 on the RunPod public ports — clients must SSH-tunnel.
#
#   ./start_xfce_vnc.sh          # install if needed, start
#   ./start_xfce_vnc.sh status
#   ./start_xfce_vnc.sh stop
set -euo pipefail

DISPLAY_NUM="${VNC_DISPLAY:-1}"
GEOMETRY="${VNC_GEOMETRY:-1920x1080}"
DEPTH="${VNC_DEPTH:-24}"
VNC_PORT=$((5900 + DISPLAY_NUM))
VNC_DIR="${HOME}/.vnc"
LOG="${VNC_DIR}/xfce_:${DISPLAY_NUM}.log"
XSTARTUP="${VNC_DIR}/xstartup"

need() {
  command -v "$1" >/dev/null 2>&1
}

vnc_bin() {
  if need tigervncserver; then
    command -v tigervncserver
  elif need vncserver; then
    command -v vncserver
  else
    return 1
  fi
}

display_up() {
  ss -lnt 2>/dev/null | grep -qE "127\\.0\\.0\\.1:${VNC_PORT}\\b" \
    || ss -lnt 2>/dev/null | grep -qE "\\[::1\\]:${VNC_PORT}\\b"
}

install_desktop() {
  if need startxfce4 && vnc_bin >/dev/null; then
    return 0
  fi
  echo "Installing XFCE + TigerVNC (first run)..."
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -qq
  apt-get install -y -qq --no-install-recommends \
    tigervnc-standalone-server tigervnc-common \
    xfce4 xfce4-terminal dbus-x11 \
    x11-xserver-utils
}

write_xstartup() {
  mkdir -p "$VNC_DIR"
  cat >"$XSTARTUP" <<'EOF'
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
[ -r "$HOME/.Xresources" ] && xrdb "$HOME/.Xresources"
export XKL_XMODMAP_DISABLE=1
export XDG_SESSION_TYPE=x11
export XDG_CURRENT_DESKTOP=XFCE
if command -v dbus-launch >/dev/null 2>&1; then
  exec dbus-launch --exit-with-session startxfce4
fi
exec startxfce4
EOF
  chmod 755 "$XSTARTUP"
}

write_passwd() {
  mkdir -p "$VNC_DIR"
  if [[ -n "${VNC_PASSWORD:-}" ]]; then
    printf '%s\n' "$VNC_PASSWORD" | vncpasswd -f >"${VNC_DIR}/passwd"
    chmod 600 "${VNC_DIR}/passwd"
    return 0
  fi
  # SSH tunnel is the auth. No VNC password unless VNC_PASSWORD is set.
  rm -f "${VNC_DIR}/passwd"
}

start_vnc() {
  if display_up; then
    echo "VNC already listening on 127.0.0.1:${VNC_PORT} (display :${DISPLAY_NUM})"
    return 0
  fi

  install_desktop
  write_xstartup
  write_passwd

  local bin
  bin="$(vnc_bin)"

  # Kill a stale :N that is not actually listening.
  "$bin" -kill ":${DISPLAY_NUM}" >/dev/null 2>&1 || true
  rm -f "/tmp/.X${DISPLAY_NUM}-lock" "/tmp/.X11-unix/X${DISPLAY_NUM}"

  local auth_args=()
  if [[ -n "${VNC_PASSWORD:-}" ]]; then
    auth_args=(-SecurityTypes VncAuth -rfbauth "${VNC_DIR}/passwd")
  else
    auth_args=(-SecurityTypes None)
  fi

  echo "Starting XFCE on :${DISPLAY_NUM} (${GEOMETRY}, localhost-only)..."
  "$bin" ":${DISPLAY_NUM}" \
    -localhost yes \
    -geometry "$GEOMETRY" \
    -depth "$DEPTH" \
    "${auth_args[@]}" \
    >"$LOG" 2>&1

  local i
  for i in $(seq 1 40); do
    if display_up; then
      echo "XFCE VNC ready on 127.0.0.1:${VNC_PORT}  (DISPLAY=:${DISPLAY_NUM})"
      echo "Tunnel from the laptop — do not publish this port:"
      echo "  ssh -N -L ${VNC_PORT}:127.0.0.1:${VNC_PORT} USER@HOST"
      echo "  then open vnc://127.0.0.1:${VNC_PORT}"
      return 0
    fi
    sleep 0.25
  done
  echo "error: VNC did not bind 127.0.0.1:${VNC_PORT}" >&2
  tail -n 40 "$LOG" >&2 || true
  exit 1
}

stop_vnc() {
  local bin
  if bin="$(vnc_bin)"; then
    "$bin" -kill ":${DISPLAY_NUM}" >/dev/null 2>&1 || true
  fi
  pkill -f "Xtigervnc :${DISPLAY_NUM}" >/dev/null 2>&1 || true
  echo "Stopped display :${DISPLAY_NUM}"
}

status_vnc() {
  if display_up; then
    echo "up  127.0.0.1:${VNC_PORT}  DISPLAY=:${DISPLAY_NUM}"
    exit 0
  fi
  echo "down  :${DISPLAY_NUM}"
  exit 1
}

case "${1:-start}" in
  start) start_vnc ;;
  stop) stop_vnc ;;
  status) status_vnc ;;
  *)
    echo "usage: $0 [start|stop|status]" >&2
    exit 2
    ;;
esac
