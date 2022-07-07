![](https://maestropandy.files.wordpress.com/2016/05/1.png?w=700)

1.	Bảng điều khiển hoặc CLI lấy thông tin đăng nhập của người dùng và thực hiện lệnh REST tới Keystone để xác thực.
2.	Keystone xác thực thông tin đăng nhập và tạo & gửi lại mã thông báo xác thực sẽ được sử dụng để gửi yêu cầu đến các Thành phần khác thông qua lệnh gọi REST.
3.	Trang tổng quan hoặc CLI chuyển đổi yêu cầu phiên bản mới được chỉ định trong biểu mẫu ‘khởi chạy phiên bản’ hoặc ‘nova-boot’ thành yêu cầu API REST và gửi đến nova-api.
4.	nova-api nhận yêu cầu và gửi yêu cầu xác thực mã thông báo xác thực và quyền truy cập tokeystone.
5.	Keystone xác thực mã thông báo và gửi tiêu đề xác thực được cập nhật với các vai trò và quyền.
6.	nova-api tương tác với nova-database.
7.	Tạo mục nhập db ban đầu cho phiên bản mới.
8.	nova-api gửi yêu cầu rpc.call đến nova-Scheduler ngoại trừ để nhận mục nhập phiên bản cập nhật với ID máy chủ được chỉ định.
9.	nova-Scheduler chọn yêu cầu từ hàng đợi.
10. nova-Scheduler tương tác với nova-database để tìm một máy chủ thích hợp thông qua lọc và cân.
11. Trả về mục nhập phiên bản đã cập nhật với ID máy chủ thích hợp sau khi lọc và cân.
12. nova-Scheduler gửi yêu cầu rpc.cast tới nova-compute để "khởi chạy phiên bản" trên máy chủ thích hợp.
13. nova-compute chọn yêu cầu từ hàng đợi.
14. nova-compute gửi yêu cầu rpc.call đến nova-wire để tìm nạp thông tin cá thể như ID máy chủ và hương vị (Ram, CPU, Đĩa).
15. Người dẫn nova chọn yêu cầu từ hàng đợi.
16. nova-wire tương tác với nova-database.
17. Trả lại thông tin cá thể.
18. nova-compute chọn thông tin cá thể từ hàng đợi.
19. nova-compute thực hiện lệnh gọi REST bằng cách chuyển mã thông báo auth-api cho nháy mắt-api để lấy nhanh URI hình ảnh theo ID hình ảnh và tải hình ảnh lên từ bộ lưu trữ hình ảnh.
20. liếc-api xác thực mã thông báo xác thực bằng keystone.
21. nova-compute lấy siêu dữ liệu hình ảnh.
22. nova-compute thực hiện lệnh gọi REST bằng cách chuyển auth-token đến Network API để phân bổ và định cấu hình mạng sao cho phiên bản đó nhận được địa chỉ IP.
23. máy chủ lượng tử xác thực mã thông báo xác thực bằng keystone.
24. nova-compute lấy thông tin mạng.
25. nova-compute thực hiện lệnh gọi REST bằng cách chuyển auth-token tới Volume API để đính kèm khối lượng vào phiên bản.
26. cinder-api xác thực mã thông báo xác thực bằng keystone.
27. nova-compute nhận thông tin lưu trữ khối.
28. nova-compute tạo dữ liệu cho trình điều khiển hypervisor và thực hiện yêu cầu trên Hypervisor (thông qua libvirt hoặc api).
