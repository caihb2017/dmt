import cv2
import numpy as np
import pdb

# 读取 BMP 格式的图像
img = cv2.imread('images/0.bmp', cv2.IMREAD_UNCHANGED)

# 检查图像是否读取成功
if img is None:
    print('Failed to read image')
    exit()

# 将图像转换为灰度图像
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 使用Otsu算法进行图像二值化
_, thresh = cv2.threshold(gray_img, 20, 200, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 提取轮廓
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_none, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


# 筛选出面积在指定范围内的轮廓
contours = [cnt for cnt in contours if 100 <= cv2.contourArea(cnt) <= 700]
contours_none = [cnt for cnt in contours_none if 100 <= cv2.contourArea(cnt) <= 700]

# 绘制轮廓和显示轮廓图
contour_img = cv2.drawContours(img, contours, -1, (255, 0, 0), 2)
cv2.imshow('contour', contour_img)

# 检测圆形轮廓
filtered_contours = []
for i in range(len(contours)):
    # Final filtering to select circular points of the calibration board
    epsilon = 0.01 * cv2.arcLength(contours[i], True)
    approx = cv2.approxPolyDP(contours[i], epsilon, True)
    if len(approx) >= 8 and len(approx) <= 30:
        area = cv2.contourArea(contours[i])
        perimeter = cv2.arcLength(contours[i], True)
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        if circularity >= 0.80:
            filtered_contours.append(contours[i])

filtered_contours_none = []
for i in range(len(contours_none)):
    # Final filtering to select circular points of the calibration board
    epsilon = 0.01 * cv2.arcLength(contours_none[i], True)
    approx = cv2.approxPolyDP(contours_none[i], epsilon, True)
    if len(approx) >= 8 and len(approx) <= 30:
        area = cv2.contourArea(contours_none[i])
        perimeter = cv2.arcLength(contours_none[i], True)
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        if circularity >= 0.80:
            filtered_contours_none.append(contours_none[i])

# 显示轮廓图和圆形图
# 观察两个轮廓线完全重合
img = cv2.drawContours(img, filtered_contours, -1, (0, 0, 255), 1)
img = cv2.drawContours(img, filtered_contours_none, -1, (255, 0, 0), 1)
cv2.imshow('contour_filter', img)
cv2.waitKey(0)

# 无法比较，两个轮廓可以顺序不同
# for i in range(len(filtered_contours)):
#     print("i=", i)
#     for j in range(len(filtered_contours[i])):
#         point1 = filtered_contours[i][j][0]
#         point2 = filtered_contours_none[i][j][0]
#         x1 = point1[0]
#         y1 = point1[1]
#         x2 = point2[0]
#         y2 = point2[1]
#         print("\tj=", j, x1, y1, "\t", x2, y2)



criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 100, 0.0001)
subpix_contours = []
for i in range(len(filtered_contours)):
    contour_corners = [filtered_contours[i][j] for j in range(len(filtered_contours[i]))]
    contour_corners = np.array(contour_corners, dtype=np.float32)
    cv2.cornerSubPix(gray_img, np.array(contour_corners), (7, 7), (-1, -1), criteria)
    subpix_contours.append(contour_corners)

subpix_contours_none = []
for i in range(len(filtered_contours_none)):
    contour_corners = [filtered_contours_none[i][j] for j in range(len(filtered_contours_none[i]))]
    contour_corners = np.array(contour_corners, dtype=np.float32)
    cv2.cornerSubPix(gray_img, np.array(contour_corners), (7, 7), (-1, -1), criteria)
    subpix_contours_none.append(contour_corners)

# 使用 cv.minEnclosingCircle() 计算圆心坐标，全部重合
# fitEllipse()拟合圆心，有两个圆心没有重合
# 先求亚像素轮廓，再椭圆拟合，有两个圆心没有重合
# 起作用的是椭圆拟合
img_simple = img.copy()
for i, cnt in enumerate(filtered_contours):
# for i, cnt in enumerate(subpix_contours):
    # (x, y), radius = cv2.minEnclosingCircle(cnt)
    # center = (int(x), int(y))
    # radius = int(radius)
    # cv2.circle(img_none, center, radius, (0, 0, 255), 2)
    # cv2.putText(img_none, str(i), center, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    ellipse = cv2.fitEllipse(cnt)
    center = tuple(map(int, ellipse[0]))
    cv2.circle(img_simple, center, 1, (0, 0, 255), 2)
    
# for i, cnt in enumerate(subpix_contours_none):
for i, cnt in enumerate(filtered_contours_none):
    # (x, y), radius = cv2.minEnclosingCircle(cnt)
    # center = (int(x), int(y))
    # radius = int(radius)
    ellipse = cv2.fitEllipse(cnt)
    center = tuple(map(int, ellipse[0]))
    cv2.circle(img_simple, center, 1, (255, 0, 0), 2)
    # cv2.putText(img_simple, str(i), center, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# 显示结果
# cv2.imshow('circle', img_simple)
cv2.waitKey(0)
cv2.destroyAllWindows()
