resource "aws_lb" "main" {
  count              = local.enable_alb ? 1 : 0
  name               = substr("${local.name_prefix}-alb", 0, 32)
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb[0].id]
  subnets            = aws_subnet.public[*].id
  tags               = local.common_tags
}

resource "aws_lb_listener" "http" {
  count             = local.enable_alb ? 1 : 0
  load_balancer_arn = aws_lb.main[0].arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/html"
      message_body = "<!DOCTYPE html><html><body style=\"font-family:system-ui;background:#0f172a;color:#e2e8f0;padding:2rem\"><h1>Not found</h1><p>Try <a href=\"/\" style=\"color:#7dd3fc\">/</a> or <a href=\"/products\" style=\"color:#7dd3fc\">/products</a>.</p></body></html>"
      status_code  = "404"
    }
  }
}

resource "aws_lb_listener_rule" "services" {
  for_each = local.enable_alb ? local.services : {}

  listener_arn = aws_lb_listener.http[0].arn
  priority     = index(keys(local.services), each.key) + 10

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.services[each.key].arn
  }

  condition {
    path_pattern {
      values = each.value.path_patterns
    }
  }
}
