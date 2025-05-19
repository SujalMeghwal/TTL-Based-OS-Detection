# TTL-Based OS Detection Script

This script leverages the TTL (Time To Live) value from ICMP ping responses to heuristically infer the operating system or device type of a remote IP address. TTL values differ by OS defaults, making this a simple yet effective technique for preliminary OS fingerprinting during penetration testing or network reconnaissance.

---

## How It Works

When a device replies to a ping request, it includes a TTL value representing the maximum number of hops the packet can take before being discarded. Different operating systems use characteristic initial TTL values (e.g., Windows typically uses 128, Linux uses 64). By capturing and analyzing this TTL, the script estimates the target OS or device.

---

## Usage and Requirements

- Supports Windows, Linux, and macOS by automatically adjusting ping command parameters.
- Requires Python 3.x.
- Must be run in an environment where ICMP (ping) requests are allowed by firewalls or network policies.
- Run the script and enter the target IP address when prompted.

---

## OS/Device Detection Based on TTL Ranges

| TTL Range            | Probable OS / Device                              |
|----------------------|--------------------------------------------------|
| 120 - 130            | Windows variants (Desktop or Server)             |
| 50 - 64              | Unix-like systems: Linux, FreeBSD, macOS, AIX   |
| Exactly 255          | Cisco network devices                             |
| Exactly 254          | Solaris or AIX                                   |
| Other TTL values     | May indicate other systems or unknown devices     |

*Note:* TTL values may vary based on network topology, firewall manipulation, or intermediate devices. This method provides a heuristic OS estimate, not a guaranteed fingerprint.

---

## Example Usage

Run the script and enter the target IP address when prompted:

```bash
$ python ttl_os_detection.py
Enter IP: 8.8.8.8
Detected TTL: 56
Running OS/device guess: Likely Unix/Linux or macOS variant
Press any key to exit...
```

## Output
The script outputs:
- The TTL value received in the ping response
- The estimated OS or device type based on TTL heuristics.
- If TTL is not detected or ping fails, the script will inform you accordingly.

Limitations
- TTL values can be altered by intermediate routers or security devices.
- Some devices or OSes may use non-standard TTL defaults.
- This method should be combined with other fingerprinting techniques for accurate OS detection.

