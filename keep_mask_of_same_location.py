#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def get_consecutive_masks(image_list, mask_list, threshold=0.5, min_overlap=0.5):
    """
    Returns a list of consecutive masks, where each mask is the union of all
    masks in the input list that contain a patch in approximately the same
    location. The approximate location is determined by thresholding the
    sum of the absolute differences between the masks and the first mask in
    the list.

    Args:
        image_list (list): A list of images.
        mask_list (list): A list of binary masks for each image in image_list.
        threshold (float): A threshold value to determine the approximate
            location of the patch. The thresholded mask is used to find the
            overlapping patches across multiple masks. Defaults to 0.5.
        min_overlap (float): The minimum overlap required for two patches to
            be considered in approximately the same location. The overlap is
            computed as the ratio of the intersection to the union of the
            two patches. Defaults to 0.5.

    Returns:
        A list of consecutive masks, where each mask is the union of all
        masks in the input list that contain a patch in approximately the
        same location.
    """
    # Compute the thresholded mask
    thresh_mask = (mask_list[0] > threshold).astype(np.uint8)
    thresh_mask = cv2.cvtColor(thresh_mask, cv2.COLOR_BGR2GRAY)
    thresh_mask = cv2.convertScaleAbs(thresh_mask)

    # Find the contours in the thresholded mask
    contours, _ = cv2.findContours(thresh_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize a dictionary to store the patches and their corresponding masks
    patch_dict = {}

    # Loop over the contours and compute the masks for each patch
    for contour in contours:
        # Compute the bounding box for the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Compute the mask for the patch
        patch_mask = np.zeros_like(mask_list[0])
        patch_mask[y:y+h, x:x+w] = 1
        patch_mask = (patch_mask > 0).astype(np.uint8)

        # Loop over the masks and check if the patch is present in approximately the same location
        for i, mask in enumerate(mask_list):
            # Compute the absolute difference between the mask and the patch
            diff = cv2.absdiff(mask, patch_mask)

            # Threshold the difference and compute the overlap between the two masks
            overlap = (diff < threshold).astype(np.uint8) * mask
            overlap_area = np.sum(overlap)
            union_area = np.sum(mask) + np.sum(patch_mask) - overlap_area
            overlap_ratio = overlap_area / union_area

            # If the overlap is greater than the minimum overlap, add the mask to the patch_dict
            if overlap_ratio >= min_overlap:
                if tuple(patch_mask.flatten()) not in patch_dict:
                    patch_dict[tuple(patch_mask.flatten())] = [mask]
                else:
                    patch_dict[tuple(patch_mask.flatten())].append(mask)

    # Combine the masks for each patch in the patch_dict
    consecutive_masks = []
    for patch, masks in patch_dict.items():
        combined_mask = np.zeros_like(masks[0])
        for mask in masks:
            combined_mask += mask
        consecutive_masks.append(combined_mask)

    return consecutive_masks

