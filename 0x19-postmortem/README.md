# Postmortem: Outage on Web Application Server

## Issue Summary

- **Duration:** May 10, 2024, 2:00 PM - May 10, 2024, 4:00 PM (UTC)
- **Impact:** The web application server experienced a complete outage, resulting in a 50% reduction in user access. Users attempting to access the application were met with connection errors or extremely slow response times.
- **Root Cause:** The outage was caused by a misconfiguration in the load balancer settings, leading to an overload on one of the application server instances.

## Timeline

- **Detection:** May 10, 2024, 2:00 PM (UTC)
  - The issue was detected when monitoring alerts indicated a significant increase in response times and error rates.
- **Actions Taken:**
  - Engineers investigated the application server logs and network traffic to identify potential causes.
  - Initial assumption pointed towards database issues due to recent database migrations.
  - As the investigation progressed, it was discovered that only one of the application server instances was overloaded.
- **Misleading Paths:**
  - Initially, the focus was on database-related issues, leading to wasted time investigating database performance.
  - There was a brief consideration of DDoS attacks due to the sudden surge in traffic, but no evidence supported this hypothesis.
- **Escalation:**
  - The incident was escalated to the DevOps team for further assistance in diagnosing the load balancer configuration.
- **Resolution:**
  - The misconfigured load balancer settings were identified and corrected, redistributing the traffic evenly across all application server instances.
  - Normal operation was restored by rolling back the load balancer configuration changes.

## Root Cause and Resolution

- **Root Cause:**
  - The root cause was traced to a misconfiguration in the load balancer, causing it to disproportionately distribute traffic to one application server instance.
  - This imbalance led to overutilization of resources on the overloaded instance, resulting in degraded performance and eventual outage.
- **Resolution:**
  - The load balancer configuration was adjusted to evenly distribute traffic among all available application server instances.
  - Additionally, monitoring alerts were configured to promptly detect and notify of any similar load imbalance issues in the future.

## Corrective and Preventative Measures

- **Improvements/Fixes:**
  - Implement automated testing for load balancer configurations to prevent similar misconfigurations in the future.
  - Enhance monitoring capabilities to provide real-time insights into server performance and traffic distribution.
- **Tasks:**
  1. Develop automated tests to validate load balancer configurations before deployment.
  2. Conduct a comprehensive review of load balancer settings to identify and rectify any potential misconfigurations.
  3. Enhance monitoring tools to include alerts for load balancer health and traffic distribution.
  4. Schedule regular load testing exercises to assess system performance under varying traffic conditions.
  
## Conclusion

The outage on the web application server was swiftly addressed through diligent investigation and corrective actions. By identifying and rectifying the misconfiguration in the load balancer, we have mitigated the risk of similar incidents occurring in the future. Moving forward, we remain committed to implementing robust monitoring and testing procedures to uphold the reliability and performance of our systems.

