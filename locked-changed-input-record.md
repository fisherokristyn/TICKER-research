# Locked Changed-Input Record — student only

Leave this record unexecuted until the instructor's AI-off procedure is satisfied. The assistant has neither authored a prediction nor executed this specific test. Ordinary automated unit tests elsewhere are distinct.

- Student-selected input and change: I selected the terminal growth rate as the single input to change in Apple's discounted cash flow model
Input: Terminal growth rate
Original value: 2.5%
New Value: 3.0%
All other assumptions will remain unchanged.
- Human-authored directional prediction, written with AI closed: I predict that increasing Apple's terminal growth rate from 2.5% to 3.0% will increase the company's enterprsie value, equity value, and intrinsic value per share. This is because a higher perpetual growth rate increases the value of future free cash flows beyond the explicit forecast period.
- Human-authored magnitude/reasoning: My current base evaluation is $126.34 per share, using the WACC of approximately 9.81%. I expect the intrinsic value to increase moderately, potentially by approximately $3-$6 per share. 
I expect this change because terminal value accounts for approximately 69.6% of the best-case enterprise vlaue. Comsequently, even a reltively small increase in perpetual growth can have a noticeable impact on the overall valuation. 
However, the higher growth rate also requires additional long-term reinvestment under the model's terminal ROIC assumption. Therefore, the increase in valuatio may be smaller than it would be if reinvestement requirements were ignored.
- Precommit timestamp and independent receipt/link:10/19/2026 08:11 am
https://github.com/fisherokristyn/TICKER-research/tree/main
- Actual execution time and command, completed by student under required conditions:10/19/2026 10:54 am
Command- pythin-B apple_controls.py
Changed input-terminal growth rate
original value-2.5%
new value-3%
- Observed result:
Proxy WACC: 9.805%
Enterprise Value: $1,870,242.2 million
Equity Value: $1,922,332.2 million
Estimated Intrinsic Value per share: $130.43
Terminal Value as percentage of enterprise value: 70.6%
Accounting Checks: passed for every forecast period
- Prediction versus outcome:
I predicted that increasing the terminal growth from 2.5% to 3.0% would increase Apple's intrinsic value by approximately $3-$6 per share.
After executing the change, the intrinsic value moved from $126.34 to $130.43, representing an increase of $4.09 per share.
The obsereved result was within my expected range.
- Student explanation: The observed change in Apple's intrinsic value reflects the sensitivty of the discounted cash flow model to long-term growth assumptions. Increasing the terminal growth rate affects the estimated value of cash flows beyond the xplicit forecast period. Becasue terminal value represents a substantial portion of Apple's overrall enterprise value, changing this assumption can materially influence the final valuation.
The actual change of $4.09 per share was consistent with my initial estimate. This demonstrates how sensitive the valuation is to assumptions about Apple's long-term performance.

- Required partner/reviewer evidence:
Reviewer name: Oliana Ozbaki oozbaki@purdue.edu
Reviwer Date: 10/19/2026 11:37 am
Response: "I think 3.0% terminal growth is on the high side but defensible. It’s below long-run nominal GDP growth and below the roughly 4% FCFF growth in your forecast years. Still, I’d use 2.5% as your base case and show 3.0% as the upside.

My main concern is sensitivity. Terminal value is 70.6% of your enterprise value, so most of the $130.43 comes from cash flows after FY2031. That’s why a 0.5-point change moved the price by about $4. 

I’d also question your WACC of 9.8%. Your notes say the beta and credit spread aren’t Apple-specific, and WACC drives so much of the value. Finally, your margin gains depend on services growing 9% a year, which is exactly where App Store regulation could hit."
My response: I appreciate my reviewer's feedback and agree that a 3.0% terminal growth rate is better treated as an upside scenario rather than my base case assumption. I will retain 2.5% as my base case and use the 3.0% scenario to demonstrate how sensitive Apple's valuation is to long-term growth expectations
My reviewer also raised a valid concern about the 9.8% proxy WACC, particularly because the beta and credit spread are not Apple specific. I will acknowledge this limitation and explain how changes in WACCcould affect the valuation. Additionally, I agree that the projected 9% annual services growth introduces risk, especially given App Store regulatory pressures. I will incorporate these concerns into my final investment recommendation and emphasize that the valuation is sensitive to growth, discount rate, and margin assumptions. 
Overall, this feedback helped me recognize the importance of distinguishing between a reasonble base case and more optimistic scenarios while being transparent about the model's limitations.

Do not replace missing evidence with generated text or a retrospective timestamp.
![alt text](image.png)