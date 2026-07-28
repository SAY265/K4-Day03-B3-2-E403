"""
🛠️ TOOL REGISTRY & SCHEMAS
Role 2: Tool & Spec Engineer

Đề tài: Trợ lý tư vấn khóa học cho sinh viên.

MỐC 2:
- Giữ nguyên đúng 6 tool đã xác định ở Mốc 1.
- Bổ sung docstring và mô tả chuẩn cho từng hàm.
- Khai báo dữ liệu khóa học giả lập.
"""

from __future__ import annotations

from typing import Any


# =========================================================
# 1. DỮ LIỆU KHÓA HỌC GIẢ LẬP
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
            "Cấu trúc dữ liệu cơ bản",
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
            "Hàm số",
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
            "Phân tích dữ liệu",
        ],
    },
    {
        "course_id": "WEB201",
        "name": "Phát triển Web Full-stack",
        "category": "Web Development",
        "level": "Intermediate",
        "credits": 4,
        "fee": 2_400_000,
        "schedule": {
            "day": "Thứ Bảy",
            "start": "13:00",
            "end": "16:00",
        },
        "prerequisites": ["CS101"],
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "Backend API",
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
            "start": "08:00",
            "end": "11:00",
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
            "Neural Networks",
            "CNN",
            "Deep Learning",
        ],
    },
]


# =========================================================
# 2. HÀM HỖ TRỢ
# =========================================================

def _normalize_text(value: str) -> str:
    """Chuẩn hóa chuỗi thành chữ thường và loại bỏ khoảng trắng thừa."""
    return " ".join(value.strip().lower().split())


def _find_course(course_id: str) -> dict[str, Any] | None:
    """Tìm một khóa học trong dữ liệu dựa trên mã khóa học."""
    normalized_id = course_id.strip().upper()

    for course in COURSE_DATABASE:
        if course["course_id"] == normalized_id:
            return course

    return None


def _format_currency(amount: int) -> str:
    """Định dạng một số nguyên thành chuỗi tiền tệ VNĐ."""
    return f"{amount:,} VNĐ"


# =========================================================
# 3. SÁU TOOL CHO AGENT
# =========================================================

def search_courses(
    keyword: str = "",
    category: str = "",
    level: str = "",
    max_fee: int | None = None,
) -> str:
    """
    Tìm kiếm các khóa học phù hợp với tiêu chí của sinh viên.

    Agent nên sử dụng tool này khi sinh viên muốn tìm khóa học
    nhưng chưa cung cấp mã khóa học cụ thể.

    Args:
        keyword:
            Từ khóa xuất hiện trong tên khóa học, lĩnh vực hoặc kỹ năng.
            Ví dụ: "Python", "Machine Learning", "Web".
        category:
            Lĩnh vực của khóa học.
            Ví dụ: "Artificial Intelligence", "Programming".
        level:
            Trình độ khóa học.
            Các giá trị phổ biến: Beginner, Intermediate, Advanced.
        max_fee:
            Học phí tối đa sinh viên có thể chi trả, đơn vị VNĐ.

    Returns:
        Chuỗi chứa danh sách khóa học phù hợp hoặc thông báo
        không tìm thấy kết quả.
    """
    matched_courses = []

    normalized_keyword = _normalize_text(keyword)
    normalized_category = _normalize_text(category)
    normalized_level = _normalize_text(level)

    for course in COURSE_DATABASE:
        searchable_content = " ".join(
            [
                course["course_id"],
                course["name"],
                course["category"],
                course["level"],
                *course["skills"],
            ]
        ).lower()

        if normalized_keyword and normalized_keyword not in searchable_content:
            continue

        if (
            normalized_category
            and normalized_category not in course["category"].lower()
        ):
            continue

        if normalized_level and normalized_level != course["level"].lower():
            continue

        if max_fee is not None and course["fee"] > max_fee:
            continue

        matched_courses.append(course)

    if not matched_courses:
        return "Không tìm thấy khóa học phù hợp."

    result = ["Danh sách khóa học phù hợp:"]

    for course in matched_courses:
        result.append(
            f"- {course['course_id']}: {course['name']} "
            f"| {course['level']} "
            f"| {_format_currency(course['fee'])}"
        )

    return "\n".join(result)


def get_course_details(course_id: str) -> str:
    """
    Lấy thông tin chi tiết của một khóa học.

    Agent nên sử dụng tool này khi cần xác minh thông tin của
    một khóa học đã biết mã.

    Args:
        course_id:
            Mã khóa học cần tra cứu.
            Ví dụ: "CS101", "AI301".

    Returns:
        Chuỗi chứa tên khóa học, lĩnh vực, trình độ, tín chỉ,
        học phí, lịch học, điều kiện tiên quyết và kỹ năng.
    """
    course = _find_course(course_id)

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
        f"Học phí: {_format_currency(course['fee'])}\n"
        f"Lịch học: {schedule['day']} "
        f"{schedule['start']}-{schedule['end']}\n"
        f"Điều kiện tiên quyết: "
        f"{', '.join(prerequisites) if prerequisites else 'Không có'}\n"
        f"Kỹ năng: {', '.join(course['skills'])}"
    )


def check_prerequisites(
    course_id: str,
    completed_courses: list[str],
) -> str:
    """
    Kiểm tra sinh viên có đáp ứng điều kiện tiên quyết hay không.

    Agent nên sử dụng tool này trước khi đề xuất sinh viên đăng ký
    một khóa học có yêu cầu môn học tiên quyết.

    Args:
        course_id:
            Mã khóa học sinh viên muốn đăng ký.
        completed_courses:
            Danh sách mã khóa học sinh viên đã hoàn thành.
            Ví dụ: ["CS101", "MATH201"].

    Returns:
        Chuỗi thông báo sinh viên đủ điều kiện hoặc danh sách
        các khóa học tiên quyết còn thiếu.
    """
    course = _find_course(course_id)

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
            f"Sinh viên đủ điều kiện đăng ký "
            f"{course['course_id']} - {course['name']}."
        )

    return (
        f"Sinh viên chưa đủ điều kiện đăng ký {course['course_id']}. "
        f"Các khóa còn thiếu: {', '.join(missing_courses)}."
    )


def check_schedule_conflict(
    course_id: str,
    unavailable_slots: list[dict[str, str]],
) -> str:
    """
    Kiểm tra lịch học có trùng với thời gian sinh viên bận hay không.

    Agent nên sử dụng tool này khi sinh viên cung cấp lịch bận
    hoặc yêu cầu chọn khóa học phù hợp với thời gian cá nhân.

    Args:
        course_id:
            Mã khóa học cần kiểm tra.
        unavailable_slots:
            Danh sách khoảng thời gian sinh viên không thể tham gia.

            Mỗi phần tử có dạng:
            {
                "day": "Thứ Bảy",
                "start": "08:00",
                "end": "10:00"
            }

    Returns:
        Chuỗi thông báo khóa học có hoặc không trùng lịch.
    """
    course = _find_course(course_id)

    if course is None:
        return f"Không tìm thấy khóa học có mã '{course_id}'."

    course_day = course["schedule"]["day"]

    for slot in unavailable_slots:
        if _normalize_text(slot["day"]) == _normalize_text(course_day):
            return (
                f"Khóa {course['course_id']} có khả năng trùng lịch "
                f"vào {course_day}."
            )

    return f"Khóa {course['course_id']} không trùng ngày sinh viên bận."


def compare_courses(course_ids: list[str]) -> str:
    """
    So sánh hai hoặc nhiều khóa học.

    Agent nên sử dụng tool này khi sinh viên đang phân vân
    giữa nhiều lựa chọn khóa học.

    Args:
        course_ids:
            Danh sách mã khóa học cần so sánh.
            Ví dụ: ["DS201", "AI301"].

    Returns:
        Chuỗi so sánh học phí, tín chỉ, trình độ, lịch học
        và điều kiện tiên quyết của các khóa.
    """
    courses = []

    for course_id in course_ids:
        course = _find_course(course_id)

        if course is None:
            return f"Không tìm thấy khóa học có mã '{course_id}'."

        courses.append(course)

    result = ["SO SÁNH KHÓA HỌC"]

    for course in courses:
        schedule = course["schedule"]

        result.append(
            f"\n{course['course_id']} - {course['name']}\n"
            f"- Trình độ: {course['level']}\n"
            f"- Tín chỉ: {course['credits']}\n"
            f"- Học phí: {_format_currency(course['fee'])}\n"
            f"- Lịch học: {schedule['day']} "
            f"{schedule['start']}-{schedule['end']}"
        )

    return "\n".join(result)


def recommend_learning_path(
    goal: str,
    completed_courses: list[str] | None = None,
) -> str:
    """
    Đề xuất lộ trình học theo mục tiêu nghề nghiệp của sinh viên.

    Agent nên sử dụng tool này khi sinh viên muốn biết nên học
    các khóa theo thứ tự nào để đạt được một mục tiêu cụ thể.

    Args:
        goal:
            Mục tiêu học tập hoặc nghề nghiệp.
            Ví dụ: "Machine Learning Engineer", "Data Analyst",
            "Web Developer".
        completed_courses:
            Danh sách mã khóa học sinh viên đã hoàn thành.

    Returns:
        Chuỗi chứa các khóa học nên hoàn thành theo thứ tự
        từ nền tảng đến nâng cao.
    """
    if completed_courses is None:
        completed_courses = []

    normalized_goal = _normalize_text(goal)

    if "machine learning" in normalized_goal:
        path = [
            "CS101",
            "MATH101",
            "MATH201",
            "DS201",
            "AI301",
            "AI401",
        ]
        goal_name = "Machine Learning Engineer"

    elif "data analyst" in normalized_goal:
        path = [
            "CS101",
            "MATH101",
            "MATH201",
            "DS201",
        ]
        goal_name = "Data Analyst"

    elif "web developer" in normalized_goal:
        path = [
            "CS101",
            "WEB201",
        ]
        goal_name = "Web Developer"

    else:
        return f"Chưa có lộ trình cho mục tiêu '{goal}'."

    completed_set = {
        course_id.strip().upper()
        for course_id in completed_courses
    }

    remaining_path = [
        course_id
        for course_id in path
        if course_id not in completed_set
    ]

    result = [f"Lộ trình đề xuất: {goal_name}"]

    for index, course_id in enumerate(remaining_path, start=1):
        course = _find_course(course_id)

        if course is not None:
            result.append(
                f"{index}. {course['course_id']} - {course['name']}"
            )

    return "\n".join(result)


# =========================================================
# 4. TOOL REGISTRY — ĐÚNG 6 TOOL
# =========================================================

AVAILABLE_TOOLS = {
    "search_courses": search_courses,
    "get_course_details": get_course_details,
    "check_prerequisites": check_prerequisites,
    "check_schedule_conflict": check_schedule_conflict,
    "compare_courses": compare_courses,
    "recommend_learning_path": recommend_learning_path,
}