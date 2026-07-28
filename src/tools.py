"""
🛠️ TOOL REGISTRY & SCHEMAS
Role 2: Tool & Spec Engineer

Các công cụ hỗ trợ ReAct Agent tư vấn khóa học cho sinh viên:
- Tìm kiếm khóa học
- Xem thông tin chi tiết
- Kiểm tra điều kiện tiên quyết
- Kiểm tra xung đột lịch học
- So sánh khóa học
- Đề xuất lộ trình học
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
# 2. HÀM HỖ TRỢ NỘI BỘ
# =========================================================

def _normalize_text(value: str) -> str:
    """
    Chuẩn hóa chuỗi phục vụ tìm kiếm.

    Args:
        value: Chuỗi cần chuẩn hóa.

    Returns:
        Chuỗi viết thường và đã loại bỏ khoảng trắng thừa.
    """
    return " ".join(value.strip().lower().split())


def _find_course(course_id: str) -> dict[str, Any] | None:
    """
    Tìm khóa học theo mã khóa học.

    Args:
        course_id: Mã khóa học.

    Returns:
        Dictionary khóa học nếu tìm thấy, ngược lại trả về None.
    """
    normalized_id = _normalize_text(course_id).upper()

    for course in COURSE_DATABASE:
        if course["course_id"].upper() == normalized_id:
            return course

    return None


def _format_currency(amount: int) -> str:
    """
    Định dạng số tiền theo đơn vị VNĐ.

    Args:
        amount: Số tiền cần định dạng.

    Returns:
        Chuỗi tiền tệ, ví dụ: 2,500,000 VNĐ.
    """
    return f"{amount:,} VNĐ"


def _format_course_summary(course: dict[str, Any]) -> str:
    """
    Chuyển thông tin khóa học thành chuỗi tóm tắt.

    Args:
        course: Dictionary chứa dữ liệu khóa học.

    Returns:
        Chuỗi tóm tắt khóa học.
    """
    schedule = course["schedule"]

    return (
        f"- {course['course_id']}: {course['name']}\n"
        f"  Lĩnh vực: {course['category']}\n"
        f"  Trình độ: {course['level']}\n"
        f"  Học phí: {_format_currency(course['fee'])}\n"
        f"  Lịch học: {schedule['day']} "
        f"{schedule['start']}-{schedule['end']}\n"
        f"  Điều kiện tiên quyết: "
        f"{', '.join(course['prerequisites']) if course['prerequisites'] else 'Không có'}"
    )


def _time_to_minutes(time_text: str) -> int:
    """
    Chuyển thời gian HH:MM sang tổng số phút.

    Args:
        time_text: Chuỗi thời gian dạng HH:MM.

    Returns:
        Tổng số phút tính từ 00:00.

    Raises:
        ValueError: Nếu thời gian không đúng định dạng.
    """
    hour_text, minute_text = time_text.split(":")
    hour = int(hour_text)
    minute = int(minute_text)

    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
        raise ValueError("Thời gian không hợp lệ.")

    return hour * 60 + minute


def _is_time_overlap(
    start_1: str,
    end_1: str,
    start_2: str,
    end_2: str,
) -> bool:
    """
    Kiểm tra hai khoảng thời gian có giao nhau hay không.

    Args:
        start_1: Thời gian bắt đầu khoảng thứ nhất.
        end_1: Thời gian kết thúc khoảng thứ nhất.
        start_2: Thời gian bắt đầu khoảng thứ hai.
        end_2: Thời gian kết thúc khoảng thứ hai.

    Returns:
        True nếu hai khoảng thời gian giao nhau, ngược lại False.
    """
    start_1_minutes = _time_to_minutes(start_1)
    end_1_minutes = _time_to_minutes(end_1)
    start_2_minutes = _time_to_minutes(start_2)
    end_2_minutes = _time_to_minutes(end_2)

    return max(start_1_minutes, start_2_minutes) < min(
        end_1_minutes,
        end_2_minutes,
    )


# =========================================================
# 3. CÁC TOOL CHO AGENT
# =========================================================

def search_courses(
    keyword: str = "",
    category: str = "",
    level: str = "",
    max_fee: int | None = None,
) -> str:
    """
    Tìm kiếm khóa học theo từ khóa, lĩnh vực, trình độ và học phí tối đa.

    Tool này nên được Agent sử dụng khi sinh viên muốn tìm khóa học phù hợp
    nhưng chưa cung cấp mã khóa học cụ thể.

    Args:
        keyword:
            Từ khóa xuất hiện trong tên khóa học, kỹ năng hoặc lĩnh vực.
            Ví dụ: "Python", "Machine Learning", "Web".
        category:
            Lĩnh vực khóa học.
            Ví dụ: "Artificial Intelligence", "Programming".
        level:
            Trình độ khóa học.
            Giá trị gợi ý: "Beginner", "Intermediate", "Advanced".
        max_fee:
            Học phí tối đa mà sinh viên có thể chi trả.
            Đơn vị: VNĐ.

    Returns:
        Danh sách khóa học phù hợp hoặc thông báo lỗi có kiểm soát.
    """
    try:
        if max_fee is not None and max_fee < 0:
            return "LỖI: Học phí tối đa không được là số âm."

        normalized_keyword = _normalize_text(keyword)
        normalized_category = _normalize_text(category)
        normalized_level = _normalize_text(level)

        if (
            not normalized_keyword
            and not normalized_category
            and not normalized_level
            and max_fee is None
        ):
            return (
                "LỖI: Cần cung cấp ít nhất một tiêu chí tìm kiếm như "
                "từ khóa, lĩnh vực, trình độ hoặc học phí tối đa."
            )

        matched_courses: list[dict[str, Any]] = []

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

            if (
                normalized_keyword
                and normalized_keyword not in searchable_content
            ):
                continue

            if (
                normalized_category
                and normalized_category
                not in course["category"].lower()
            ):
                continue

            if (
                normalized_level
                and normalized_level != course["level"].lower()
            ):
                continue

            if max_fee is not None and course["fee"] > max_fee:
                continue

            matched_courses.append(course)

        if not matched_courses:
            return (
                "KHÔNG TÌM THẤY: Không có khóa học nào phù hợp "
                "với các tiêu chí đã cung cấp."
            )

        result_lines = [
            f"Tìm thấy {len(matched_courses)} khóa học phù hợp:"
        ]

        for course in matched_courses:
            result_lines.append(_format_course_summary(course))

        return "\n\n".join(result_lines)

    except (TypeError, ValueError) as error:
        return f"LỖI DỮ LIỆU: Không thể tìm kiếm khóa học: {error}"
    except Exception as error:
        return f"LỖI HỆ THỐNG: Công cụ tìm kiếm khóa học thất bại: {error}"


def get_course_details(course_id: str) -> str:
    """
    Lấy thông tin chi tiết của một khóa học theo mã khóa học.

    Tool này nên được Agent gọi khi cần xác minh lịch học, học phí,
    tín chỉ, kỹ năng hoặc điều kiện tiên quyết của một khóa học cụ thể.

    Args:
        course_id:
            Mã khóa học cần tra cứu.
            Ví dụ: "CS101", "AI301".

    Returns:
        Thông tin đầy đủ của khóa học hoặc thông báo lỗi.
    """
    try:
        if not isinstance(course_id, str) or not course_id.strip():
            return "LỖI: Mã khóa học không được để trống."

        course = _find_course(course_id)

        if course is None:
            return (
                f"KHÔNG TÌM THẤY: Không tồn tại khóa học có mã "
                f"'{course_id}'."
            )

        schedule = course["schedule"]

        return (
            f"THÔNG TIN KHÓA HỌC\n"
            f"- Mã khóa học: {course['course_id']}\n"
            f"- Tên khóa học: {course['name']}\n"
            f"- Lĩnh vực: {course['category']}\n"
            f"- Trình độ: {course['level']}\n"
            f"- Số tín chỉ: {course['credits']}\n"
            f"- Học phí: {_format_currency(course['fee'])}\n"
            f"- Lịch học: {schedule['day']} "
            f"{schedule['start']}-{schedule['end']}\n"
            f"- Điều kiện tiên quyết: "
            f"{', '.join(course['prerequisites']) if course['prerequisites'] else 'Không có'}\n"
            f"- Kỹ năng đạt được: {', '.join(course['skills'])}"
        )

    except Exception as error:
        return (
            f"LỖI HỆ THỐNG: Không thể lấy thông tin khóa học: {error}"
        )


def check_prerequisites(
    course_id: str,
    completed_courses: list[str],
) -> str:
    """
    Kiểm tra sinh viên có đáp ứng điều kiện tiên quyết của khóa học hay không.

    Tool này phải được Agent gọi trước khi đề xuất sinh viên đăng ký
    một khóa học có prerequisite.

    Args:
        course_id:
            Mã khóa học cần kiểm tra.
        completed_courses:
            Danh sách mã các khóa học sinh viên đã hoàn thành.
            Ví dụ: ["CS101", "MATH201"].

    Returns:
        Kết quả đủ điều kiện hoặc danh sách khóa học còn thiếu.
    """
    try:
        if not isinstance(course_id, str) or not course_id.strip():
            return "LỖI: Mã khóa học không được để trống."

        if not isinstance(completed_courses, list):
            return (
                "LỖI: completed_courses phải là một danh sách mã khóa học."
            )

        course = _find_course(course_id)

        if course is None:
            return (
                f"KHÔNG TÌM THẤY: Không tồn tại khóa học có mã "
                f"'{course_id}'."
            )

        normalized_completed = {
            str(item).strip().upper()
            for item in completed_courses
            if str(item).strip()
        }

        prerequisites = {
            item.upper() for item in course["prerequisites"]
        }

        if not prerequisites:
            return (
                f"ĐỦ ĐIỀU KIỆN: Khóa {course['course_id']} - "
                f"{course['name']} không yêu cầu môn học tiên quyết."
            )

        missing_courses = prerequisites - normalized_completed

        if not missing_courses:
            return (
                f"ĐỦ ĐIỀU KIỆN: Sinh viên đã hoàn thành đầy đủ "
                f"điều kiện tiên quyết của khóa {course['course_id']}."
            )

        return (
            f"CHƯA ĐỦ ĐIỀU KIỆN: Sinh viên còn thiếu các khóa học: "
            f"{', '.join(sorted(missing_courses))}. "
            f"Cần hoàn thành các khóa này trước khi đăng ký "
            f"{course['course_id']}."
        )

    except Exception as error:
        return (
            f"LỖI HỆ THỐNG: Không thể kiểm tra điều kiện tiên quyết: "
            f"{error}"
        )


def check_schedule_conflict(
    course_id: str,
    unavailable_slots: list[dict[str, str]],
) -> str:
    """
    Kiểm tra lịch học của khóa có trùng với thời gian sinh viên bận hay không.

    Tool này nên được Agent gọi khi sinh viên cung cấp lịch bận hoặc yêu cầu
    chỉ tìm khóa học trong những thời điểm nhất định.

    Args:
        course_id:
            Mã khóa học cần kiểm tra.
        unavailable_slots:
            Danh sách các khoảng thời gian sinh viên không thể tham gia.

            Mỗi phần tử có dạng:
            {
                "day": "Thứ Bảy",
                "start": "08:00",
                "end": "10:00"
            }

    Returns:
        Kết quả có hoặc không có xung đột lịch học.
    """
    try:
        if not isinstance(course_id, str) or not course_id.strip():
            return "LỖI: Mã khóa học không được để trống."

        if not isinstance(unavailable_slots, list):
            return "LỖI: unavailable_slots phải là một danh sách."

        course = _find_course(course_id)

        if course is None:
            return (
                f"KHÔNG TÌM THẤY: Không tồn tại khóa học có mã "
                f"'{course_id}'."
            )

        course_schedule = course["schedule"]
        conflicts: list[str] = []

        for index, slot in enumerate(unavailable_slots, start=1):
            if not isinstance(slot, dict):
                return (
                    f"LỖI: Khoảng thời gian thứ {index} phải là dictionary."
                )

            required_fields = {"day", "start", "end"}

            if not required_fields.issubset(slot):
                return (
                    f"LỖI: Khoảng thời gian thứ {index} phải có đủ "
                    f"day, start và end."
                )

            same_day = (
                _normalize_text(slot["day"])
                == _normalize_text(course_schedule["day"])
            )

            if same_day and _is_time_overlap(
                course_schedule["start"],
                course_schedule["end"],
                slot["start"],
                slot["end"],
            ):
                conflicts.append(
                    f"{slot['day']} {slot['start']}-{slot['end']}"
                )

        if conflicts:
            return (
                f"TRÙNG LỊCH: Khóa {course['course_id']} học vào "
                f"{course_schedule['day']} "
                f"{course_schedule['start']}-{course_schedule['end']}, "
                f"bị trùng với thời gian bận: {', '.join(conflicts)}."
            )

        return (
            f"KHÔNG TRÙNG LỊCH: Khóa {course['course_id']} học vào "
            f"{course_schedule['day']} "
            f"{course_schedule['start']}-{course_schedule['end']}."
        )

    except (TypeError, ValueError) as error:
        return f"LỖI DỮ LIỆU LỊCH: {error}"
    except Exception as error:
        return (
            f"LỖI HỆ THỐNG: Không thể kiểm tra xung đột lịch học: "
            f"{error}"
        )


def compare_courses(course_ids: list[str]) -> str:
    """
    So sánh nhiều khóa học theo học phí, tín chỉ, trình độ và lịch học.

    Tool này nên được Agent gọi khi sinh viên đang phân vân giữa
    hai hoặc nhiều khóa học.

    Args:
        course_ids:
            Danh sách mã khóa học cần so sánh.
            Ví dụ: ["DS201", "AI301"].

    Returns:
        Bảng so sánh dạng văn bản hoặc thông báo lỗi.
    """
    try:
        if not isinstance(course_ids, list):
            return "LỖI: course_ids phải là một danh sách."

        normalized_ids = [
            str(course_id).strip().upper()
            for course_id in course_ids
            if str(course_id).strip()
        ]

        if len(normalized_ids) < 2:
            return "LỖI: Cần ít nhất hai khóa học để so sánh."

        found_courses: list[dict[str, Any]] = []
        missing_ids: list[str] = []

        for course_id in normalized_ids:
            course = _find_course(course_id)

            if course is None:
                missing_ids.append(course_id)
            else:
                found_courses.append(course)

        if missing_ids:
            return (
                f"KHÔNG TÌM THẤY: Các mã khóa học không tồn tại: "
                f"{', '.join(missing_ids)}."
            )

        lines = ["SO SÁNH KHÓA HỌC"]

        for course in found_courses:
            schedule = course["schedule"]

            lines.append(
                f"\n{course['course_id']} - {course['name']}\n"
                f"- Trình độ: {course['level']}\n"
                f"- Tín chỉ: {course['credits']}\n"
                f"- Học phí: {_format_currency(course['fee'])}\n"
                f"- Lịch học: {schedule['day']} "
                f"{schedule['start']}-{schedule['end']}\n"
                f"- Điều kiện tiên quyết: "
                f"{', '.join(course['prerequisites']) if course['prerequisites'] else 'Không có'}"
            )

        cheapest_course = min(
            found_courses,
            key=lambda item: item["fee"],
        )

        highest_credit_course = max(
            found_courses,
            key=lambda item: item["credits"],
        )

        lines.append(
            f"\nNHẬN XÉT TỰ ĐỘNG\n"
            f"- Học phí thấp nhất: {cheapest_course['course_id']} "
            f"({_format_currency(cheapest_course['fee'])})\n"
            f"- Số tín chỉ cao nhất: "
            f"{highest_credit_course['course_id']} "
            f"({highest_credit_course['credits']} tín chỉ)"
        )

        return "\n".join(lines)

    except Exception as error:
        return f"LỖI HỆ THỐNG: Không thể so sánh khóa học: {error}"


def recommend_learning_path(
    goal: str,
    completed_courses: list[str] | None = None,
) -> str:
    """
    Đề xuất lộ trình học dựa trên mục tiêu nghề nghiệp của sinh viên.

    Tool này phù hợp với câu hỏi nhiều bước, ví dụ sinh viên muốn trở thành
    Machine Learning Engineer hoặc Web Developer nhưng chưa biết nên học
    môn nào trước.

    Args:
        goal:
            Mục tiêu học tập hoặc nghề nghiệp.
            Ví dụ: "Machine Learning Engineer", "Data Analyst",
            "Web Developer".
        completed_courses:
            Danh sách mã khóa học sinh viên đã hoàn thành.

    Returns:
        Lộ trình khóa học theo thứ tự từ nền tảng đến nâng cao.
    """
    try:
        if not isinstance(goal, str) or not goal.strip():
            return "LỖI: Mục tiêu học tập không được để trống."

        if completed_courses is None:
            completed_courses = []

        if not isinstance(completed_courses, list):
            return (
                "LỖI: completed_courses phải là một danh sách mã khóa học."
            )

        normalized_goal = _normalize_text(goal)
        completed_set = {
            str(course_id).strip().upper()
            for course_id in completed_courses
            if str(course_id).strip()
        }

        if any(
            keyword in normalized_goal
            for keyword in [
                "machine learning",
                "ai engineer",
                "trí tuệ nhân tạo",
                "artificial intelligence",
            ]
        ):
            path = ["CS101", "MATH101", "MATH201", "DS201", "AI301", "AI401"]
            goal_name = "Machine Learning / AI Engineer"

        elif any(
            keyword in normalized_goal
            for keyword in [
                "data analyst",
                "phân tích dữ liệu",
                "data science",
            ]
        ):
            path = ["CS101", "MATH101", "MATH201", "DS201"]
            goal_name = "Data Analyst"

        elif any(
            keyword in normalized_goal
            for keyword in [
                "web developer",
                "full-stack",
                "fullstack",
                "lập trình web",
            ]
        ):
            path = ["CS101", "WEB201"]
            goal_name = "Web Developer"

        else:
            return (
                f"KHÔNG HỖ TRỢ: Chưa có lộ trình được định nghĩa "
                f"cho mục tiêu '{goal}'. "
                f"Các mục tiêu hiện hỗ trợ gồm Machine Learning Engineer, "
                f"Data Analyst và Web Developer."
            )

        remaining_path = [
            course_id
            for course_id in path
            if course_id not in completed_set
        ]

        if not remaining_path:
            return (
                f"HOÀN THÀNH LỘ TRÌNH: Sinh viên đã hoàn thành toàn bộ "
                f"các khóa học cần thiết cho mục tiêu {goal_name}."
            )

        result_lines = [
            f"LỘ TRÌNH ĐỀ XUẤT: {goal_name}",
            "Các khóa học nên hoàn thành theo thứ tự:",
        ]

        for index, course_id in enumerate(remaining_path, start=1):
            course = _find_course(course_id)

            if course is not None:
                result_lines.append(
                    f"{index}. {course['course_id']} - "
                    f"{course['name']} ({course['level']})"
                )

        if completed_set:
            result_lines.append(
                "\nCác khóa học đã hoàn thành và được bỏ qua: "
                + ", ".join(sorted(completed_set))
            )

        return "\n".join(result_lines)

    except Exception as error:
        return f"LỖI HỆ THỐNG: Không thể xây dựng lộ trình học: {error}"


# =========================================================
# 4. TOOL REGISTRY
# =========================================================

# Chỉ những hàm được đăng ký tại đây mới được Agent phép gọi.
AVAILABLE_TOOLS = {
    "search_courses": search_courses,
    "get_course_details": get_course_details,
    "check_prerequisites": check_prerequisites,
    "check_schedule_conflict": check_schedule_conflict,
    "compare_courses": compare_courses,
    "recommend_learning_path": recommend_learning_path,
}


# =========================================================
# 5. TOOL SCHEMAS
# =========================================================

# Schema mô tả tool để Role 4 truyền cho mô hình AI.
# Cấu trúc tương thích với dạng function calling phổ biến.
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_courses",
            "description": (
                "Tìm khóa học theo từ khóa, lĩnh vực, trình độ "
                "hoặc học phí tối đa."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": (
                            "Từ khóa liên quan đến tên, kỹ năng "
                            "hoặc lĩnh vực khóa học."
                        ),
                    },
                    "category": {
                        "type": "string",
                        "description": "Lĩnh vực của khóa học.",
                    },
                    "level": {
                        "type": "string",
                        "enum": [
                            "Beginner",
                            "Intermediate",
                            "Advanced",
                        ],
                        "description": "Trình độ của khóa học.",
                    },
                    "max_fee": {
                        "type": "integer",
                        "minimum": 0,
                        "description": "Học phí tối đa, đơn vị VNĐ.",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_course_details",
            "description": (
                "Lấy thông tin chi tiết của khóa học bằng mã khóa học."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "string",
                        "description": "Mã khóa học, ví dụ AI301.",
                    }
                },
                "required": ["course_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_prerequisites",
            "description": (
                "Kiểm tra sinh viên có đáp ứng điều kiện tiên quyết "
                "của khóa học không."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "string",
                        "description": "Mã khóa học cần kiểm tra.",
                    },
                    "completed_courses": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "Danh sách mã khóa học sinh viên "
                            "đã hoàn thành."
                        ),
                    },
                },
                "required": [
                    "course_id",
                    "completed_courses",
                ],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_schedule_conflict",
            "description": (
                "Kiểm tra lịch khóa học có trùng với thời gian "
                "sinh viên bận hay không."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "string",
                        "description": "Mã khóa học cần kiểm tra.",
                    },
                    "unavailable_slots": {
                        "type": "array",
                        "description": (
                            "Danh sách các khoảng thời gian "
                            "sinh viên không thể tham gia."
                        ),
                        "items": {
                            "type": "object",
                            "properties": {
                                "day": {
                                    "type": "string",
                                    "description": "Ngày trong tuần.",
                                },
                                "start": {
                                    "type": "string",
                                    "description": (
                                        "Giờ bắt đầu dạng HH:MM."
                                    ),
                                },
                                "end": {
                                    "type": "string",
                                    "description": (
                                        "Giờ kết thúc dạng HH:MM."
                                    ),
                                },
                            },
                            "required": [
                                "day",
                                "start",
                                "end",
                            ],
                        },
                    },
                },
                "required": [
                    "course_id",
                    "unavailable_slots",
                ],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compare_courses",
            "description": (
                "So sánh từ hai khóa học trở lên theo học phí, "
                "tín chỉ, trình độ và lịch học."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "course_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 2,
                        "description": (
                            "Danh sách mã khóa học cần so sánh."
                        ),
                    }
                },
                "required": ["course_ids"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "recommend_learning_path",
            "description": (
                "Đề xuất lộ trình học theo mục tiêu nghề nghiệp "
                "và các khóa sinh viên đã hoàn thành."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "goal": {
                        "type": "string",
                        "description": (
                            "Mục tiêu nghề nghiệp hoặc học tập."
                        ),
                    },
                    "completed_courses": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "Danh sách mã khóa học đã hoàn thành."
                        ),
                    },
                },
                "required": ["goal"],
            },
        },
    },
]


# =========================================================
# 6. HÀM THỰC THI TOOL AN TOÀN
# =========================================================

def execute_tool(tool_name: str, arguments: dict[str, Any]) -> str:
    """
    Thực thi một tool đã đăng ký trong AVAILABLE_TOOLS.

    Hàm này giúp Role 4 không cần trực tiếp truy cập hoặc gọi hàm bằng eval.
    Tuyệt đối không dùng eval() để thực thi tool do Agent yêu cầu.

    Args:
        tool_name:
            Tên tool mà Agent muốn gọi.
        arguments:
            Dictionary chứa tham số truyền vào tool.

    Returns:
        Kết quả từ tool hoặc thông báo lỗi có kiểm soát.
    """
    try:
        if not isinstance(tool_name, str) or not tool_name.strip():
            return "LỖI: Tên tool không được để trống."

        if not isinstance(arguments, dict):
            return "LỖI: Arguments của tool phải là dictionary."

        tool = AVAILABLE_TOOLS.get(tool_name)

        if tool is None:
            available_names = ", ".join(AVAILABLE_TOOLS.keys())

            return (
                f"LỖI: Tool '{tool_name}' không tồn tại. "
                f"Các tool hợp lệ gồm: {available_names}."
            )

        return tool(**arguments)

    except TypeError as error:
        return (
            f"LỖI THAM SỐ: Không thể gọi tool '{tool_name}': {error}"
        )
    except Exception as error:
        return (
            f"LỖI HỆ THỐNG: Tool '{tool_name}' thực thi thất bại: "
            f"{error}"
        )


# =========================================================
# 7. TEST NHANH FILE TOOLS.PY
# =========================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TEST 1: Tìm khóa học Machine Learning")
    print("=" * 60)
    print(
        search_courses(
            keyword="Machine Learning",
            max_fee=3_000_000,
        )
    )

    print("\n" + "=" * 60)
    print("TEST 2: Kiểm tra prerequisite AI301")
    print("=" * 60)
    print(
        check_prerequisites(
            course_id="AI301",
            completed_courses=["CS101"],
        )
    )

    print("\n" + "=" * 60)
    print("TEST 3: Kiểm tra trùng lịch")
    print("=" * 60)
    print(
        check_schedule_conflict(
            course_id="AI301",
            unavailable_slots=[
                {
                    "day": "Thứ Bảy",
                    "start": "09:00",
                    "end": "10:00",
                }
            ],
        )
    )

    print("\n" + "=" * 60)
    print("TEST 4: Xây dựng lộ trình AI")
    print("=" * 60)
    print(
        recommend_learning_path(
            goal="Machine Learning Engineer",
            completed_courses=["CS101"],
        )
    )

    print("\n" + "=" * 60)
    print("TEST 5: Gọi tool không tồn tại")
    print("=" * 60)
    print(
        execute_tool(
            tool_name="delete_database",
            arguments={},
        )
    )