# 🤖 DYNAMICAL SYSTEMS ANALYSIS & DESIGN ✏️
The objective of this workshop is to incorporate methods from systems science and cybernetic theory into the autonomous agent, understanding real-time changes, feedback loops and nonlinear behaviors.<br>

Therefore, we made some changes to the system diagram. We adjusted the feedbacks and incorporated new adaptive logic for Insight Engine, also, we add external actor (specialist) who helps to supervise and evaluate the recomendations of the system. In addition, we added new inputs that are very important for improving the walker recommendations, such as training data and the patient's medical history.<br>
![System_diagram_v2](diagrams/system_diagram.png)

## 🌀 System Dynamics Analysis 🌀
### Causal Model as a Basis for Simulation
The causal model developed represents a complex sensor-assisted gait assessment system, in which key components such as data collection, storage, processing by an inference engine (Insight Engine) and feedback to the patient through personalized recommendations are identified. <br>

This model allows the identification of feedback loops, nonlinear relationships and temporal dependencies, which helps to analyze their evolution over time, even without detailed quantitative simulation. <br>
![Feedback_loop_InightEngine](diagrams/causal_diagram.png)
To understand the diagram properly, it is important to recognize the symbols that compose it. The opposing triangles (in the shape of a valve) represent activities or processes that mark a transition between stages of the system. The squares represent stocks, meaning elements that accumulate or maintain a state over time. Arrows indicate relationships of influence: they point from the variable that has the effect to the variable that receives it.
#### 📊 Non-linear Factors
The following is a list of variables or relationships in the model that show non-linear behavior, which means that their effect is not proportional to their cause:
- **Fatigue vs. Patient Gait**:
The relationship between fatigue and patient gait quality presents a clear non-linearity, as the impact of fatigue is not proportional in all phases of exercise or rehabilitation. It should also be taken into account that factors such as the patient's habits, sleep quality and previous activities influence the way patient gaits. Initially, small increases in fatigue may have minimal effects on gait; however, once a certain physiological threshold is crossed, the deterioration in gait quality rapidly intensifies. This behavior implies that the system must be especially sensitive to detect early signs of fatigue, as a delay in intervention can trigger disproportionately negative consequences, such as loss of stability, risk of falls or aggravation of previous injuries. 
- **Environment vs. Data Collection**: 
The relationship between environmental conditions and data capture accuracy is clearly non-linear, as small changes in factors such as lighting, temperature, unexpected interference or environmental stability may not have an immediate impact on the sensors; however, when certain critical limits are exceeded, data quality degrades abruptly and significantly. For example, a small drop in illumination can be tolerated by optical sensors, but a more pronounced drop can lead to inaccurate readings or outright loss of data.
- **Level of Personal Recomendations vs. Effectiveness of the intervention**
This relationship represents a nonlinear learning curve, where at first, more general adjustments may have limited impact. However, as the system collects more patient-specific data (such as medical history, treatment responses, training data), smaller changes in personalization, made by the Insight Engine and specialist assessment, can generate much more noticeable improvements in efficacy. This reflects the fact that personalization does not always have an immediate impact, but once the system begins to understand the patient better, the return on that personalization increases exponentially.

### ⏱️ Time-Dependent Factors
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

## 🔄 Feedback Loop Refinement 🔄
The system now has two new feedback cycles. The first one is present in the Insight engine, in which it adjusts itself based on the data it processes and the results it generates to the point where it can be considered as self-learning by the element. On the other hand, the second cycle consists of a signal given by an external element considered a specialist, indicating how good the results of the Insight engine are. This last cycle can be considered a reward signal that indicates precisely and in real time how good a recommendation was in a specific case. <br>
![Feedback_loop_InightEngine](diagrams/feedback_loops.png)

### Stability and Convergence
One of these is the BIBO (Bounded Input, Bounded Output) stability, which refers to the fact that any bounded input expects a similarly bounded output. That is to say, in our agent we expect recommendations focused on physical aspects, since the input of the system is mostly physical data of the patient. On the other hand, the motor of the system agent starts being trained, so experience, time and reward signals present a convergent behavior since its outputs will be stabilizing as it learns and its number of errors decreases. In the same way, if the physical results of the patients improve thanks to the recommendations of the system, this indicates that the outputs of the system are stabilizing. <br>
