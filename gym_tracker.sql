-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th5 11, 2024 lúc 06:29 AM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `gym_tracker`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `excercises`
--

CREATE TABLE `excercises` (
  `excercise_id` int(11) NOT NULL,
  `excercise_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `excercises`
--

INSERT INTO `excercises` (`excercise_id`, `excercise_name`) VALUES
(1, 'Dumbblle Curl'),
(2, 'Front Dumbbler Rais'),
(3, 'Dumbble Squat');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `sets`
--

CREATE TABLE `sets` (
  `set_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `workout_id` int(11) NOT NULL,
  `excercise_id` int(11) NOT NULL,
  `repetition_left` int(11) NOT NULL,
  `repetition_right` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `sets`
--

INSERT INTO `sets` (`set_id`, `user_id`, `workout_id`, `excercise_id`, `repetition_left`, `repetition_right`) VALUES
(1, 3, 6, 1, 1, 2),
(2, 3, 6, 1, 0, 2),
(3, 3, 6, 3, 0, 0),
(4, 3, 7, 1, 3, 15),
(5, 3, 7, 2, 0, 1),
(6, 3, 11, 2, 3, 4),
(7, 3, 12, 3, 0, 0);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `account_name` varchar(255) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT '0000-00-00 00:00:00.000000' ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `user`
--

INSERT INTO `user` (`id`, `account_name`, `user_name`, `password`, `created_at`) VALUES
(3, 'lehanh', 'Lê Văn Hạnh', '1', '2024-04-29 11:42:09.837073');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `workouts`
--

CREATE TABLE `workouts` (
  `workout_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `workout_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `workouts`
--

INSERT INTO `workouts` (`workout_id`, `user_id`, `workout_date`) VALUES
(6, 3, '2024-04-29'),
(7, 3, '2024-04-30'),
(8, 3, '2024-05-01'),
(9, 3, '2024-05-02'),
(10, 3, '2024-05-03'),
(11, 3, '2024-05-05'),
(12, 3, '2024-05-10');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `excercises`
--
ALTER TABLE `excercises`
  ADD PRIMARY KEY (`excercise_id`);

--
-- Chỉ mục cho bảng `sets`
--
ALTER TABLE `sets`
  ADD PRIMARY KEY (`set_id`),
  ADD KEY `workout_id` (`workout_id`),
  ADD KEY `excercise_id` (`excercise_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Chỉ mục cho bảng `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `workouts`
--
ALTER TABLE `workouts`
  ADD PRIMARY KEY (`workout_id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `excercises`
--
ALTER TABLE `excercises`
  MODIFY `excercise_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT cho bảng `sets`
--
ALTER TABLE `sets`
  MODIFY `set_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT cho bảng `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT cho bảng `workouts`
--
ALTER TABLE `workouts`
  MODIFY `workout_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `sets`
--
ALTER TABLE `sets`
  ADD CONSTRAINT `sets_ibfk_1` FOREIGN KEY (`workout_id`) REFERENCES `workouts` (`workout_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `sets_ibfk_2` FOREIGN KEY (`excercise_id`) REFERENCES `excercises` (`excercise_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `sets_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `workouts`
--
ALTER TABLE `workouts`
  ADD CONSTRAINT `workouts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
