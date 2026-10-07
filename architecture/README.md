# Architecture as Code

`reference-architecture.yaml` is the AP supplier query agent design from Lab 5.1. Validate it with:
```
PYTHONPATH=shared python -c "from playbook.platform import architecture; r,md,mm=architecture('architecture/reference-architecture.yaml'); print(r.to_dict()['status']); print(mm)"
```
The Mermaid output is the editable source for the book's architecture figures.
