import { useAuth } from "../context/AuthProvider";
import { useNavigate } from 'react-router-dom';

function Dashboard() {
    const {logout} = useAuth();
    const navigate = useNavigate();

    console.log("inside dashboard");
    
    const handleSubmit = () => {
        logout();
        navigate("/login");
    }

    return (<>
        <h1>Welcome to the dashboard</h1>
        <button onClick={handleSubmit}>Logout</button>
        <a href="/tester">go to tester</a>

    </>);
}

export default Dashboard;