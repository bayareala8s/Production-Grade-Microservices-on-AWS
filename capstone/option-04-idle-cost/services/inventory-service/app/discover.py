import json
import os
from typing import Any

import httpx

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SCAN_MODE = os.getenv("SCAN_MODE", "mock")  # mock | aws


def mock_resources() -> list[dict[str, Any]]:
    """Teaching fixtures — idle NAT/ALB/ECS/EIP like a forgotten lab weekend."""
    return [
        {
            "resource_type": "NAT",
            "resource_id": "nat-0idlelab001",
            "region": AWS_REGION,
            "name": "ms-course-dev-nat",
            "signals": {
                "bytes_out_7d": 0,
                "hours_running": 168,
            },
        },
        {
            "resource_type": "ALB",
            "resource_id": "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/ms-course-dev-alb/abc",
            "region": AWS_REGION,
            "name": "ms-course-dev-alb",
            "signals": {
                "healthy_hosts": 0,
                "request_count_7d": 0,
            },
        },
        {
            "resource_type": "ECS_SERVICE",
            "resource_id": "order-service",
            "region": AWS_REGION,
            "name": "order-service",
            "signals": {
                "desired_count": 1,
                "avg_cpu_7d": 0.2,
            },
        },
        {
            "resource_type": "EIP",
            "resource_id": "eipalloc-0orphan001",
            "region": AWS_REGION,
            "name": "unattached-eip",
            "signals": {
                "associated": False,
            },
        },
    ]


def aws_resources() -> list[dict[str, Any]]:
    """Read-only discovery — never mutates resources."""
    import boto3

    resources: list[dict[str, Any]] = []
    ec2 = boto3.client("ec2", region_name=AWS_REGION)
    elbv2 = boto3.client("elbv2", region_name=AWS_REGION)
    ecs = boto3.client("ecs", region_name=AWS_REGION)

    for nat in ec2.describe_nat_gateways().get("NatGateways", []):
        if nat.get("State") != "available":
            continue
        resources.append(
            {
                "resource_type": "NAT",
                "resource_id": nat["NatGatewayId"],
                "region": AWS_REGION,
                "name": nat["NatGatewayId"],
                "signals": {"bytes_out_7d": 0, "hours_running": 24},
            }
        )

    for alb in elbv2.describe_load_balancers().get("LoadBalancers", []):
        resources.append(
            {
                "resource_type": "ALB",
                "resource_id": alb["LoadBalancerArn"],
                "region": AWS_REGION,
                "name": alb.get("LoadBalancerName"),
                "signals": {"healthy_hosts": 0, "request_count_7d": 0},
            }
        )

    for eip in ec2.describe_addresses().get("Addresses", []):
        resources.append(
            {
                "resource_type": "EIP",
                "resource_id": eip.get("AllocationId", eip.get("PublicIp")),
                "region": AWS_REGION,
                "name": eip.get("PublicIp"),
                "signals": {"associated": bool(eip.get("AssociationId"))},
            }
        )

    for cluster in ecs.list_clusters().get("clusterArns", []):
        services = ecs.list_services(cluster=cluster).get("serviceArns", [])
        if not services:
            continue
        for svc in ecs.describe_services(cluster=cluster, services=services).get("services", []):
            resources.append(
                {
                    "resource_type": "ECS_SERVICE",
                    "resource_id": svc["serviceName"],
                    "region": AWS_REGION,
                    "name": svc["serviceName"],
                    "signals": {
                        "desired_count": svc.get("desiredCount", 0),
                        "avg_cpu_7d": 1.0,
                    },
                }
            )
    return resources


def discover() -> tuple[str, list[dict[str, Any]]]:
    if SCAN_MODE == "aws":
        try:
            return "aws", aws_resources()
        except Exception:
            return "mock_fallback", mock_resources()
    return "mock", mock_resources()


def publish_scan_completed(scan_id: str, aws_account_id: str, resources: list[dict[str, Any]]) -> None:
    url = os.getenv("ANALYZER_EVENT_URL", "http://localhost:8033/events")
    payload = {
        "source": "capstone.finops.inventory",
        "detail-type": "InventoryScanCompleted",
        "detail": {
            "scan_id": scan_id,
            "aws_account_id": aws_account_id,
            "resources": [
                {
                    "resource_type": r["resource_type"],
                    "resource_id": r["resource_id"],
                    "region": r.get("region", AWS_REGION),
                    "name": r.get("name"),
                    "signals": r.get("signals", {}),
                }
                for r in resources
            ],
        },
    }
    try:
        with httpx.Client(timeout=15.0) as client:
            client.post(url, json=payload).raise_for_status()
    except Exception:
        pass
