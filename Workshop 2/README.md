# 🤖 DYNAMICAL SYSTEMS ANALYSIS & DESIGN ✏️
The objective of this workshop is to incorporate methods from systems science and cybernetic theory into the autonomous agent, understanding real-time changes, feedback loops and nonlinear behaviors.<br>

Therefore, we made some changes to the system diagram. We adjusted the feedbacks and incorporated new adaptive logic for Insight Engine, also, we add external actor (specialist) who helps to supervise and evaluate the recomendations of the system. In addition, we added new inputs that are very important for improving the walker recommendations, such as training data and the patient's medical history.<br>

##  System Dynamics Analysis
### Causal Model as a Basis for Simulation
The causal model developed represents a complex sensor-assisted gait assessment system, in which key components such as data collection, storage, processing by an inference engine (Insight Engine) and feedback to the patient through personalized recommendations are identified. <br>

This model allows the identification of feedback loops, nonlinear relationships and temporal dependencies, which helps to analyze their evolution over time, even without detailed quantitative simulation. <br>

####  Non-linear Factors
The following is a list of variables or relationships in the model that show non-linear behavior, which means that their effect is not proportional to their cause:
- **Fatigue vs. Patient Gait**:
The relationship between fatigue and patient gait quality presents a clear non-linearity, as the impact of fatigue is not proportional in all phases of exercise or rehabilitation. It should also be taken into account that factors such as the patient's habits, sleep quality and previous activities influence the way patient gaits. Initially, small increases in fatigue may have minimal effects on gait; however, once a certain physiological threshold is crossed, the deterioration in gait quality rapidly intensifies. This behavior implies that the system must be especially sensitive to detect early signs of fatigue, as a delay in intervention can trigger disproportionately negative consequences, such as loss of stability, risk of falls or aggravation of previous injuries. 
- **Environment vs. Data Collection**: 
The relationship between environmental conditions and data capture accuracy is clearly non-linear, as small changes in factors such as lighting, temperature, unexpected interference or environmental stability may not have an immediate impact on the sensors; however, when certain critical limits are exceeded, data quality degrades abruptly and significantly. For example, a small drop in illumination can be tolerated by optical sensors, but a more pronounced drop can lead to inaccurate readings or outright loss of data.
- **Level of Personal Recomendations vs. Effectiveness of the intervention**
This relationship represents a nonlinear learning curve, where at first, more general adjustments may have limited impact. However, as the system collects more patient-specific data (such as medical history, treatment responses, training data), smaller changes in personalization, made by the Insight Engine and specialist assessment, can generate much more noticeable improvements in efficacy. This reflects the fact that personalization does not always have an immediate impact, but once the system begins to understand the patient better, the return on that personalization increases exponentially.

### Time-Dependent Factor
They are those that change over time and whose evolution influences the behavior of the system.

- Level of fatigue: Increases or decreases according to sleep, physical activity and habits, and changes constantly with the patient's condition.
- Muscle activity: Varies over time depending on physical condition, injuries and gait quality.
- Patient gait: Evolves progressively with the patient's condition, fatigue, injuries and recommendations.
- Injuries: Accumulates or decreases over time depending on activity and effectiveness of recommendations.
- Storage capacity: Changes dynamically as more data is collected and processed.
- Sensor quality: May degrade with use or change due to maintenance/calibration over time.
- Environment: Although external, its conditions (temperature, light, interference) are constantly changing and impact the system.
- Data collection: Occurs continuously during monitoring, affecting system dynamics.
- Personal Recommendation: Changes over time according to new data, feedback and system learning.
- Insight Engine processing: Evolves according to the volume and quality of data received and accumulated personalization.

## Feedback Loop Refinement
