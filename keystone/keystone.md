1. Keystone
- Keystone là một Openstack project cung cấp các dịch vụ Identify, Token, Catalog, Policy cho các dịch vụ khác trong Openstack. Keystone Gồm hai phiên bản:
    + User Managerment: Keystone giúp xác thực tài khoản người dụng và chỉ định xem người dùng có quyền gì.
    + Service Catalog: Cung cấp một danh mục các dịch vụ sẵn sàng cùng với các API endpoint để truy cập các dịch vụ đó.

2. Basic Concepts
- Identity: Dịch vụ Identity cung cấp xác thực thông tin và dữ liệu về người dùng và nhóm
	+ Users: đại diện các cá thể sử dụng API cá nhân
	+ Groups: là các container chứa các users
- Resource: cung cấp dữ liệu cho các projects và domains
	+ Projects: sử dụng để nhóm hoặc cô lập tài nguyên, hoặc định danh các đối tượng. Tùy thuộc vào nhà quản lý
	+ Domains: Là high-level container cho projects, groups và users. Domains có thể được sử dụng như một cách để ủy quyền quản lý tài nguyên OpenStack. Người dùng trong một miền vẫn có thể truy cập tài nguyên trong một miền khác, nếu được cấp phép
- Assignment: cung cấp dữ liệu cho roles và roles assignments
	+ Roles: quyết định mức độ ủy quyền mà người dùng cuối có thể nhận được, roles có thể được cấp ở cấp độ domain hoặc cấp độ project
- Token:  xác thực và quản lý mã thông báo được sử dụng để xác thực yêu cầu sau khi thông tin đăng nhập của người dùng đã được xác minh.
- catalog:
	+Service catalog là cần thiết cho OpenStack cloud. Nó chứa URLs and endpoint của các Cloud services khác nhau. Không có catalog, users và applications không biết nơi để route các requests để tạo VMs hoặc store objects. Service catalog chia thành a list of endpoint, mỗi endpoint chia nhỏ thành admin URL, internal URL, và public URL, có thể giống nhau.

3. Identity
3.1 SQL
- Keystone bao gồm tùy chọn lưu trữ your actors (Users và Groups) trong SQL; hỗ trợ databases bao gồm MySQL, PostgreSQL, và DB2. Keystone sẽ lưu trữ information như name, password, và description.
- Setting cho database phải được chỉ định trong Keystone’s configuration file. Về bản chất, Keystone hoạt động như Identity Provider.
- Ưu và nhược điểm của SQL Indentity option:
Pros:
	+ Dễ cài đặt
	+ Quản lý users và groups thông qua OpenStack APIs
Cons:
	+ Keystone không thể trở thành Identity Provider.
	+ Hỗ trợ weak password ( no password rotation và no password recovery)
