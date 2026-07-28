"""
🛠️ TOOL REGISTRY & SCHEMAS
Role 2: Tool Engineer

Các công cụ hỗ trợ Agent tư vấn khóa học cho sinh viên.
"""

from typing import Any


# =========================================================
# DỮ LIỆU KHÓA HỌC GIẢ LẬP
# =========================================================

COURSE_DATABASE: list[dict[str, Any]] = [
    {
        "course_id": "CS101",
        "name": "Lập trình Python cơ bản",
        "category": "Programming",
        "level": "Beginner",
        "credits": 3,
        "fee": 1_500_000,
        "schedule": {
            "day": "Thứ Ba",
            "start": "18:00",
            "end": "20:00",
        },
        "prerequisites": [],
        "skills": [
            "Python",
            "Tư duy lập trình",
        ],
    },
    {
        "course_id": "MATH101",
        "name": "Toán đại cương",
        "category": "Mathematics",
        "level": "Beginner",
        "credits": 3,
        "fee": 1_400_000,
        "schedule": {
            "day": "Thứ Hai",
            "start": "18:00",
            "end": "20:00",
        },
        "prerequisites": [],
        "skills": [
            "Đại số",
            "Tư duy toán học",
        ],
    },
    {
        "course_id": "MATH201",
        "name": "Xác suất và thống kê",
        "category": "Mathematics",
        "level": "Intermediate",
        "credits": 3,
        "fee": 1_800_000,
        "schedule": {
            "day": "Thứ Năm",
            "start": "18:00",
            "end": "20:00",
        },
        "prerequisites": ["MATH101"],
        "skills": [
            "Xác suất",
            "Thống kê",
        ],
    },
    {
        "course_id": "DS201",
        "name": "Phân tích dữ liệu với Python",
        "category": "Data Science",
        "level": "Intermediate",
        "credits": 3,
        "fee": 2_200_000,
        "schedule": {
            "day": "Thứ Bảy",
            "start": "13:00",
            "end": "16:00",
        },
        "prerequisites": ["CS101", "MATH101"],
        "skills": [
            "Pandas",
            "NumPy",
            "Data Visualization",
        ],
    },
    {
        "course_id": "AI301",
        "name": "Nhập môn Machine Learning",
        "category": "Artificial Intelligence",
        "level": "Intermediate",
        "credits": 4,
        "fee": 2_800_000,
        "schedule": {
            "day": "Thứ Bảy",
            "start": "08:00",
            "end": "11:00",
        },
        "prerequisites": ["CS101", "MATH201"],
        "skills": [
            "Machine Learning",
            "Tiền xử lý dữ liệu",
            "Đánh giá mô hình",
        ],
    },
    {
        "course_id": "AI401",
        "name": "Deep Learning nâng cao",
        "category": "Artificial Intelligence",
        "level": "Advanced",
        "credits": 4,
        "fee": 3_500_000,
        "schedule": {
            "day": "Chủ Nhật",
            "start": "08:00",
            "end": "11:00",
        },
        "prerequisites": ["AI301", "MATH201"],
        "skills": [
            "Neural Network",
            "CNN",
            "Deep Learning",
        ],
    },
]


# =========================================================
# HÀM HỖ TRỢ
# =========================================================

def find_course(course_id: str) -> dict[str, Any] | None:
    """
    Tìm một khóa học theo mã khóa học.

    Args:
        course_id: Mã khóa học, ví dụ AI301.

    Returns:
        Dictionary khóa học nếu tìm thấy, ngược lại trả về None.
    """
    normalized_id = course_id.strip().upper()

    for course in COURSE_DATABASE:
        if course["course_id"] == normalized_id:
            return course

    return None


# =========================================================
# TOOL 1: SEARCH COURSES
# =========================================================

def search_courses(keyword: str) -> str:
    """
    Tìm khóa học theo từ khóa.

    Tool này được sử dụng khi sinh viên muốn tìm các khóa học theo
    tên, lĩnh vực hoặc kỹ năng.

    Args:
        keyword:
            Từ khóa tìm kiếm.
            Ví dụ: Python, Machine Learning, Data Science.

    Returns:
        Danh sách các khóa học phù hợp.
    """
    keyword_lower = keyword.strip().lower()
    matched_courses = []

    for course in COURSE_DATABASE:
        searchable_text = " ".join(
            [
                course["course_id"],
                course["name"],
                course["category"],
                *course["skills"],
            ]
        ).lower()

        if keyword_lower in searchable_text:
            matched_courses.append(course)

    if not matched_courses:
        return f"Không tìm thấy khóa học phù hợp với từ khóa '{keyword}'."

    result = ["Danh sách khóa học phù hợp:"]

    for course in matched_courses:
        result.append(
            f"- {course['course_id']}: {course['name']} "
            f"| Trình độ: {course['level']} "
            f"| Học phí: {course['fee']:,} VNĐ"
        )

    return "\n".join(result)


# =========================================================
# TOOL 2: GET COURSE DETAILS
# =========================================================

def get_course_details(course_id: str) -> str:
    """
    Lấy thông tin chi tiết của khóa học.

    Args:
        course_id:
            Mã khóa học.
            Ví dụ: CS101 hoặc AI301.

    Returns:
        Thông tin chi tiết của khóa học.
    """
    course = find_course(course_id)

    if course is None:
        return f"Không tìm thấy khóa học có mã '{course_id}'."

    schedule = course["schedule"]
    prerequisites = course["prerequisites"]

    return (
        f"Mã khóa học: {course['course_id']}\n"
        f"Tên khóa học: {course['name']}\n"
        f"Lĩnh vực: {course['category']}\n"
        f"Trình độ: {course['level']}\n"
        f"Tín chỉ: {course['credits']}\n"
        f"Học phí: {course['fee']:,} VNĐ\n"
        f"Lịch học: {schedule['day']} "
        f"{schedule['start']}-{schedule['end']}\n"
        f"Điều kiện tiên quyết: "
        f"{', '.join(prerequisites) if prerequisites else 'Không có'}\n"
        f"Kỹ năng: {', '.join(course['skills'])}"
    )


# =========================================================
# TOOL 3: CHECK PREREQUISITES
# =========================================================

def check_prerequisites(
    course_id: str,
    completed_courses: list[str],
) -> str:
    """
    Kiểm tra điều kiện tiên quyết của một khóa học.

    Args:
        course_id:
            Mã khóa học cần kiểm tra.
        completed_courses:
            Danh sách mã khóa học sinh viên đã hoàn thành.

    Returns:
        Kết quả sinh viên đủ hoặc chưa đủ điều kiện đăng ký.
    """
    course = find_course(course_id)

    if course is None:
        return f"Không tìm thấy khóa học có mã '{course_id}'."

    completed_set = {
        item.strip().upper()
        for item in completed_courses
    }

    missing_courses = [
        prerequisite
        for prerequisite in course["prerequisites"]
        if prerequisite not in completed_set
    ]

    if not missing_courses:
        return (
            f"Sinh viên đủ điều kiện đăng ký khóa "
            f"{course['course_id']} - {course['name']}."
        )

    return (
        f"Sinh viên chưa đủ điều kiện đăng ký {course['course_id']}. "
        f"Các khóa còn thiếu: {', '.join(missing_courses)}."
    )


# =========================================================
# TOOL REGISTRY
# =========================================================

AVAILABLE_TOOLS = {
    "search_courses": search_courses,
    "get_course_details": get_course_details,
    "check_prerequisites": check_prerequisites,
}