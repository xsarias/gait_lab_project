# 🤖 GAIT LABORATORY AGENT SYSTEMS DESIGN ✏️
This agent has a particular architecture, so is important to define all components, sensors, actuators, inputs, outputs, all of these help to design a system diagram with the relationships, modules and data flow. <br>
## System design
![system_diagram](GLA_system_diagram.jpg)
<br>
### Motion Acquisition System (Dynamic module)
Motion Acquisition System is a module of the Gait Laboratory Agent that captures dynamic biomechanical signals from the body of a subject. These signals allow for analyzing how the body moves, how much force is applied, how muscles are activated, and how the musculoskeletal system reacts during gait or a specific physical activity.  <br>
This module has the following **sensors**:
- **Reinforcement Platforms:** Measure the forces that the body exerts against the ground during walking. Identifying imbalances, gait patterns, or overload in any limb. Provides data like moments and force.
- **Transducers:** Transform physical signals (such as pressure or vibration) into electrical signals that can be analyzed. Allows for precise measurement of mechanical interactions, useful for detecting anomalies.
- **Electromyography (EMG):** Records the electrical activity of muscles as they contract. Detects muscle imbalances, levels of exertion, and coordination between muscles. Provides information about the electrical potentials that reflect muscle activation.
