def recommend(gait_class):
    """Generate medical recommendations based on the detected abnormality."""
    recommendations = {
        "Normal": {
            "abnormality": "Normal Gait",
            "description": "Your gait appears normal, indicating good posture and musculoskeletal health. No corrective actions are required.",
            "exercises": "There are no specific exercises needed, but regular walking and maintaining an active lifestyle is beneficial.",
            "advice": "Continue maintaining a healthy posture and stay active to support overall well-being."
        },
        "Limping": {
            "abnormality": "Limping",
            "description": "Limping may be caused by muscle weakness, joint pain, or past injuries. It can affect mobility and lead to long-term complications if untreated.",
            "exercises": "Try leg raises to strengthen the quadriceps and calf stretches to improve flexibility. These exercises help restore strength and balance.",
            "advice": "If the limping persists or worsens, consult a physiotherapist for a proper diagnosis and personalized rehabilitation plan."
        },
        "Slouch": {
            "abnormality": "Slouching",
            "description": "Slouching is often caused by weak core muscles and poor posture habits. Over time, it can lead to back pain and decreased mobility.",
            "exercises": "Engage in core-strengthening exercises like planks and back extensions. Postural awareness drills can also help improve alignment.",
            "advice": "Be mindful of your posture while sitting and standing. Consider ergonomic adjustments at work or home to promote better spinal alignment."
        },
        "No Arm Swing": {
            "abnormality": "Reduced Arm Swing",
            "description": "A lack of arm swing during walking may indicate stiffness, neurological conditions, or lack of coordination.",
            "exercises": "Perform shoulder mobility exercises and dynamic arm swings to improve coordination and flexibility.",
            "advice": "If you experience difficulty swinging your arms naturally, consider consulting a physical therapist for further evaluation."
        },
        "Concriduction": {
            "abnormality": "Unusual Gait Pattern",
            "description": "This condition suggests irregular movement patterns that may stem from neurological or muscular issues.",
            "exercises": "Engage in balance and coordination drills, such as single-leg stands and controlled stepping exercises.",
            "advice": "Consult a specialist if the issue persists, as it may require further medical assessment and targeted therapy."
        }
    }
    
    result = recommendations.get(gait_class, {
        "abnormality": "Unknown",
        "description": "No specific information available.",
        "exercises": "Consult a healthcare professional for tailored exercises.",
        "advice": "Seek medical guidance for a proper diagnosis."
    })
    
    return f"""
    Abnormality Detected: {result['abnormality']}
    
    Explanation: {result['description']}
    
    Recommended Exercises: {result['exercises']}
    
    Advice: {result['advice']}
    """