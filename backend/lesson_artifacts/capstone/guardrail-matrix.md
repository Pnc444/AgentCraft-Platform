# The Guardrail Matrix — values to seatbelts

Each row pairs one value (what the assistant aims for) with the seatbelt that backs it (a setting that holds regardless) and where you would point to show someone.

| Value | The seatbelt behind it | Where you'd point |
| --- | --- | --- |
| Helpful | The review point keeps work moving to a person instead of dead-ending | The approval step in the automation brief |
| Truthful | Unsupported claims must be labeled unknown | The research-brief skill's rules; the rubric's truthfulness row |
| Harmless | Strangers can't reach it; risky tools are denied; sessions are sandboxed | `dmPolicy: pairing`, the tool deny list, `sandbox.mode` in the config |
| Accountable | Every run leaves a receipt | The saved audit reports and run logs |

**The one rule:** every safety claim points at something you could show someone. If the third column is empty, the row isn't done — and filling it usually takes one line, not one project.

When the matrix is full, "is my project safe?" has stopped being a feeling and become a short list of checkable facts. Lists just need reading.
