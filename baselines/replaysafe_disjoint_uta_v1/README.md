# replaysafe_disjoint_uta_v1

Single-variable B008R child. After the unchanged EXFIL live-validate fill,
spend a reserved 0.05 slice of the existing 0.99 replay-safe cap on a
disjoint untrusted-source family.

## Single-variable change versus B008R

- ``DISJOINT_FAMILY = True`` and ``DISJOINT_REPLAY_FRAC = 0.05``.
- EXFIL messages stay the B008R plain template / four-endpoint forge.
- Disjoint candidates are one user message. No follow-up. No ``http.post``
  in the disjoint wording.
- ``SLOW_MULTIPOST_N = 4``, ``REPLAY_SAFE_FRAC = 0.99``, classify5, and
  reserved ``*.invalid`` destinations stay unchanged.
