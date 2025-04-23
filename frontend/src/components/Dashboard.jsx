import { useAuth } from "../context/AuthProvider";
import { useNavigate } from 'react-router-dom';
import { useEffect } from "react";
import apiClient from "../api/api";

function Dashboard() {
    const { logout } = useAuth();
    const navigate = useNavigate();

    const checkAwsCred = async () => {
        try {
            const response = await apiClient.get("/aws_cred/status");
            const is_aws_cred_valid = response.isUserAwsHandlerSet;
            return is_aws_cred_valid;
        }
        catch (error) {
            console.error("Full error:", error);
            if (error.response?.status == 401) {
                navigate("/login");
            }
            else {
                alert("We are facing server errors. Try Again Later");
            }
        }
    }


    useEffect(() => {
        checkAwsCred().then((res) => {
            const is_aws_cred_valid = res;
            console.log(is_aws_cred_valid);
            if (is_aws_cred_valid) {
            }
            else {
                navigate("/aws_cred/setup");
            }
        }).catch((err) => {
            console.log(err);
        })


    }, []);

    const logoutHandler = () => {
        logout();
        navigate("/login");
    }

    return (<>
        <h1>Welcome to the dashboard</h1>
        <button onClick={logoutHandler}>Logout</button>
        <a href="/tester">go to tester</a>

    </>);
}

export default Dashboard;