import subprocess
import re
import platform
import sys

def get_ttl_from_ping(ip: str, count=1, timeout=2) -> int | None:
    """
    Pings the target IP and extracts the TTL value from the response.
    Supports Windows, Linux, and macOS platforms.
    Returns TTL as integer if found, else None.
    """
    # Determine platform-specific ping parameters
    param_count = '-n' if platform.system().lower() == 'windows' else '-c'
    param_timeout = '-w' if platform.system().lower() == 'windows' else '-W'

    # Build the ping command
    cmd = ['ping', param_count, str(count), param_timeout, str(timeout), ip]

    try:
        # Run the ping command
        completed_process = subprocess.run(
            cmd, capture_output=True, text=True, check=True
        )
        output = completed_process.stdout.lower()

        # Regex to find TTL; flexible for Windows/Linux/macOS outputs
        # Windows: TTL=128
        # Linux/macOS: ttl=64 or ttl 64
        ttl_search = re.search(r'ttl[=:\s]?(\d+)', output)

        if ttl_search:
            return int(ttl_search.group(1))
        else:
            return None
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Ping command failed: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        return None


def identify_os_from_ttl(ttl: int) -> str:
    """
    Maps TTL values to probable OS/device types.
    Uses TTL ranges for better heuristic detection.
    """
    if ttl >= 128 and ttl <= 255:
        if ttl == 255:
            return "Cisco Device"
        elif ttl >= 128 and ttl < 256:
            return "Windows OS (likely Windows Server or Desktop)"
    elif ttl >= 64 and ttl < 128:
        if ttl == 64:
            return "Linux/FreeBSD/macOS/Unix-like"
        elif ttl == 100:
            return "IBM OS/2"
        elif ttl == 127 or ttl == 190:
            return "macOS"
    elif ttl >= 30 and ttl < 64:
        if ttl == 50:
            return "Windows 95/98/ME"
        elif ttl == 60:
            return "AIX"
        elif ttl == 48:
            return "BSDI"
        elif ttl == 30:
            return "SunOS"
    elif ttl >= 200 and ttl < 256:
        if ttl == 240:
            return "Novell"
        elif ttl == 254:
            return "Solaris/AIX"
        elif ttl == 200:
            return "HP-UX"
    # Fallback range check (TTL generally starts at 64, 128, 255 depending on OS)
    if 50 <= ttl <= 64:
        return "Likely Unix/Linux or macOS variant"
    if 120 <= ttl <= 130:
        return "Likely Windows variant"
    return "Unknown OS or device"


def main():
    ip = input("Enter IP: ").strip()
    if not ip:
        print("No IP entered. Exiting.")
        return

    ttl_value = get_ttl_from_ping(ip)

    if ttl_value is None:
        print("Cannot detect OS, TTL value not found or ping failed.")
    else:
        os_guess = identify_os_from_ttl(ttl_value)
        print(f"Detected TTL: {ttl_value}")
        print(f"Running OS/device guess: {os_guess}")

    input("Press any key to exit...")


if __name__ == '__main__':
    main()
