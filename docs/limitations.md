# Limitations

## System Limitations

### 1. Synthetic Data
All curriculum data, course structures, and student records are **synthetic prototype data**, not real KDU data. Results cannot be assumed to represent real academic outcomes.

### 2. Static Weight System
Specialization weights are fixed, expert-assigned values. They do not adapt to new evidence or student outcomes. Different weight assignments could produce different recommendations.

### 3. No Longitudinal Tracking
The system evaluates a student's profile at a point in time. It does not track performance trends, improvement trajectories, or predict future academic performance.

### 4. Binary Interest Model
Interests are binary (selected/not selected). A student cannot express "strongly interested" vs. "somewhat interested" — the interest vector is {0, 1} per dimension.

### 5. Single-User Prototype
The application is designed for one student at a time. There is no multi-user session management, authentication, or concurrent access handling.

### 6. Missing Subject Area Assumption
When a subject area has no completed courses, the system excludes it and renormalizes. This is correct behavior per the specification, but it means early-stage students with few courses may see volatile recommendations as they complete more courses.

### 7. ML Enhancement Accuracy
The Decision Tree classifier achieves ~53% accuracy on 6 classes (vs. ~17% chance). While it learns meaningful patterns, this moderate accuracy reflects:
- Synthetic data distribution
- Inherent overlap between specialization profiles
- Limited feature space (average marks only)

The ML enhancement is explicitly experimental and never replaces the core recommendation engine.

### 8. No Official Curriculum Verification
Course structures, prerequisite chains, and grading scales are prototype approximations. They have not been verified against official KDU curriculum documentation.

### 9. Prototype Grading Scale
The grading scale used (A+ through F with specific ranges) is a prototype scale, not verified as KDU's official grading policy.

### 10. No Real-World Validation
The system has been tested with synthetic data and manual scenarios but has not been validated with real students or real academic outcomes.

## Mitigation

- All limitations are disclosed in the UI and documentation
- Recommendations are framed as "academic decision support" not authoritative decisions
- The system explicitly states when evidence is limited
- Weights and thresholds are configurable for adjustment
- The prototype is designed to be demonstrated and explained, not deployed as-is
