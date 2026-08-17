from decimal import Decimal
from typing import Any

# Static rate card (us-east-1 teaching estimates — not a bill)
HOURS_PER_MONTH = Decimal("730")
RATES = {
    "NAT": Decimal("0.045") * HOURS_PER_MONTH,  # ~$32.85
    "ALB": Decimal("0.0225") * HOURS_PER_MONTH,  # ~$16.43
    "ECS_SERVICE": Decimal("10.00"),  # rough Fargate task
    "EIP": Decimal("0.005") * HOURS_PER_MONTH,  # ~$3.65 unattached
}


def score_resource(resource: dict[str, Any]) -> dict[str, Any] | None:
    rtype = resource["resource_type"]
    signals = resource.get("signals") or {}
    rid = resource["resource_id"]

    if rtype == "NAT" and signals.get("bytes_out_7d", 1) == 0:
        return {
            "resource_type": rtype,
            "resource_id": rid,
            "idle_score": Decimal("0.95"),
            "estimated_monthly_usd": RATES["NAT"].quantize(Decimal("0.01")),
            "reason": "NAT Gateway with near-zero traffic (7d)",
        }
    if rtype == "ALB" and signals.get("healthy_hosts", 1) == 0:
        return {
            "resource_type": rtype,
            "resource_id": rid,
            "idle_score": Decimal("0.90"),
            "estimated_monthly_usd": RATES["ALB"].quantize(Decimal("0.01")),
            "reason": "ALB with 0 healthy targets",
        }
    if rtype == "ECS_SERVICE":
        desired = int(signals.get("desired_count", 0))
        cpu = float(signals.get("avg_cpu_7d", 100))
        if desired >= 1 and cpu < 1.0:
            return {
                "resource_type": rtype,
                "resource_id": rid,
                "idle_score": Decimal("0.75"),
                "estimated_monthly_usd": RATES["ECS_SERVICE"].quantize(Decimal("0.01")),
                "reason": f"ECS service desired={desired} with ~{cpu}% avg CPU",
            }
    if rtype == "EIP" and not signals.get("associated", True):
        return {
            "resource_type": rtype,
            "resource_id": rid,
            "idle_score": Decimal("0.99"),
            "estimated_monthly_usd": RATES["EIP"].quantize(Decimal("0.01")),
            "reason": "Unattached Elastic IP",
        }
    return None
