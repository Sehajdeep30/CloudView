import { useAuth } from "../context/AuthProvider";
import { useNavigate } from 'react-router-dom';
import { useState,useEffect } from "react";
import { checkAwsCred } from "./SetAwsCred/AwsCredsUtils";


function Dashboard() {
    const { logout } = useAuth();
    const navigate = useNavigate();


    useEffect(() => {
        const verify = async () => {
          try {
            const isValid = await checkAwsCred();
            console.log("AWS cred valid?", isValid);
            if (!isValid) {
              alert(
                "Your AWS account is not connected. Redirecting you to setup page…"
              );
              navigate("/aws_cred/setup");
            }
          } catch (err) {
            console.error("Error verifying AWS creds:", err);
          }
          finally{
          }
        };

        verify();
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