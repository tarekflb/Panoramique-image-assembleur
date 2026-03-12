import cv2
import numpy as np

def trim(frame):

    if not np.sum(frame[0]):
        return trim(frame[1:])

    if not np.sum(frame[-1]):
        return trim(frame[0:-1])

    if not np.sum(frame[:,0]):
        return trim(frame[:,1:])

    if not np.sum(frame[:,-1]):
        return trim(frame[:,:-1])

    return frame


def stitch(img_base, img_to_warp):
    
    """Stitch img_to_warp onto img_base.

    The function matches features between the two images, estimates a homography,
    warps the second image into the first image's coordinate system, and then
    blends/crops the result.
    """

    if img_base is None or img_to_warp is None:
        raise ValueError("One of the input images is None")

    gray_base = cv2.cvtColor(img_base, cv2.COLOR_BGR2GRAY)
    gray_warp = cv2.cvtColor(img_to_warp, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create()

    # keypoints
    kpb, desb = sift.detectAndCompute(gray_base, None)
    kpw, desw = sift.detectAndCompute(gray_warp, None)

    # affichage keypoints (facultatif)
    cv2.imshow("keypoints_base", cv2.drawKeypoints(img_base, kpb, None))
    cv2.waitKey(0)

    cv2.imshow("keypoints_warp", cv2.drawKeypoints(img_to_warp, kpw, None))
    cv2.waitKey(0)

    matcher = cv2.BFMatcher()
    matches = matcher.knnMatch(desw, desb, k=2)  # warp -> base

    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)

    draw_params = dict(matchColor=(0,255,0),
                       singlePointColor=None,
                       flags=2)

    img_matches = cv2.drawMatches(img_to_warp, kpw, img_base, kpb, good, None, **draw_params)

    cv2.imshow("matches", img_matches)
    cv2.waitKey(0)

    MIN_MATCH_COUNT = 10

    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kpw[m.queryIdx].pt for m in good]).reshape(-1,1,2)
        dst_pts = np.float32([kpb[m.trainIdx].pt for m in good]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        h_base, w_base = img_base.shape[:2]
        h_warp, w_warp = img_to_warp.shape[:2]
        out_w = w_base + w_warp
        out_h = max(h_base, h_warp)

        dst = cv2.warpPerspective(img_to_warp, M, (out_w, out_h))
        dst[0:h_base, 0:w_base] = img_base

        result = trim(dst)

        cv2.imshow("stitched_result", result)
        cv2.waitKey(0)

        return result

    else:
        print("Not enough matches")
        return img_base


# ------------------------------
# Chargement des images
# ------------------------------

img1 = cv2.imread("image0.jpg")
img2 = cv2.imread("image1.jpg")
img3 = cv2.imread("image2.jpg")

# ------------------------------
# Stitch progressif
# ------------------------------

result = stitch(img1, img2)

result = stitch(result, img3)

cv2.imshow("final panorama", result)
cv2.waitKey(0)

cv2.imwrite("panorama.jpg", result)
