"""
🛠️ TOOL REGISTRY & SCHEMAS
Role 2: Tool & Spec Engineer

Đề tài: Trợ lý tư vấn khóa học cho sinh viên.

MỐC 1:
Liệt kê các công cụ mà ReAct Agent sẽ sử dụng.
"""


# =========================================================
# DANH SÁCH 6 TOOL DỰ KIẾN
# =========================================================

# 1. search_courses
#    Tìm kiếm khóa học theo từ khóa, lĩnh vực, trình độ
#    hoặc mức học phí tối đa.

# 2. get_course_details
#    Tra cứu thông tin chi tiết của một khóa học
#    dựa trên mã khóa học.

# 3. check_prerequisites
#    Kiểm tra sinh viên có đáp ứng các môn học
#    tiên quyết của một khóa học hay không.

# 4. check_schedule_conflict
#    Kiểm tra lịch học của khóa có trùng với
#    thời gian sinh viên bận hay không.

# 5. compare_courses
#    So sánh hai hoặc nhiều khóa học theo học phí,
#    tín chỉ, trình độ và lịch học.

# 6. recommend_learning_path
#    Đề xuất lộ trình học dựa trên mục tiêu nghề nghiệp
#    và các khóa sinh viên đã hoàn thành.


AVAILABLE_TOOLS = {}