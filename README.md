# Rating Product & Sorting Reviews in Amazon

## Project Description
This project aims to address two significant problems in e-commerce: calculating product ratings accurately based on customer feedback and sorting reviews effectively. By solving these issues, we can enhance customer satisfaction, improve product visibility for sellers, and ensure a seamless shopping experience for buyers.

## Problem Statement
Accurate computation of post-sale ratings for products is one of the most critical challenges in e-commerce. Resolving this issue can lead to greater customer satisfaction, better product visibility for sellers, and a smooth shopping experience for buyers. Another problem is the proper ranking of reviews; misleading reviews can adversely affect sales, resulting in financial loss and customer attrition.

## Dataset
The dataset used in this project contains Amazon product reviews with various metadata, particularly focusing on electronic products with the highest number of reviews. The dataset includes the following features:

- `reviewerID`: User ID
- `asin`: Product ID
- `reviewerName`: Username
- `helpful`: Helpful rating degree
- `reviewText`: Review text
- `overall`: Product rating
- `summary`: Review summary
- `unixReviewTime`: Review time in Unix timestamp
- `reviewTime`: Raw review time
- `day_diff`: Number of days since the review
- `helpful_yes`: Number of times the review was found helpful
- `total_vote`: Total votes on the review

## Implementation
The implementation involves several steps:

1. **Calculate Average Rating Based on Current Reviews and Compare with Existing Average Rating**
   - Calculate the overall average rating.
   - Compute a time-based weighted average rating using historical review data.

2. **Identify 20 Reviews to be Displayed on the Product Detail Page**
   - Create a `helpful_no` variable to count non-helpful reviews.
   - Calculate scores based on helpfulness to rank the reviews effectively.

3. **Scoring Functions**
   - Implement scoring functions such as Wilson Lower Bound to assess the quality of reviews.

By leveraging these methods, we effectively compute ratings and rank the reviews, enhancing the user's shopping experience and ensuring a more accurate representation of product quality.
