import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import awsBasicPolicies from './iam_data.js';
import {PermissionsHandler,RoleHandler,useAwsCredService } from './AwsCredsUtils.jsx';

function SetAwsCred() {
    const [selectedActions, setSelectedActions] = useState([]);
    const [isPermissionInput, setIsPermissionInput] = useState(true);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [roleArn, setRoleArn] = useState("");
    const [launchUrl, setLaunchUrl] = useState("");
    const [finalPermissions, setFinalPermissions] = useState([]);
    const [successMsg,setSuccessMsg] = useState("");

    const { createLaunchUrl, addRole } = useAwsCredService();
    const navigate = useNavigate();


    const toggleAction = (actionKey) => {
        setSelectedActions((prev) =>
            prev.includes(actionKey)
                ? prev.filter((k) => k !== actionKey)
                : [...prev, actionKey]
        );
    };

    const handlePermissionSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        // Flatten all perms for each selected actionKey
        const policy_arns = selectedActions.flatMap((actionKey) => {
            const [service, category] = actionKey.split(".");
            return awsBasicPolicies[service][category] || [];
        });
        if (policy_arns.length == 0) {
            setError("Atleast One Permission Required!");
            setLoading(false);
            return;
        }
        setError("");
        try {
            const url = await createLaunchUrl(policy_arns);
            setLaunchUrl(url);
            setIsPermissionInput(false);
            setFinalPermissions(policy_arns);
        }
        catch (error) {
            console.log(error);
            setError(error.response?.data?.detail || "Something went wrong");
        }
        finally {
            setLoading(false);
        }

    };

    const handleRoleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        // Flatten all perms for each selected actionKey
        if (!roleArn) {
            setError("Role Arn cannot be empty");
            setLoading(false);
            return;
        }
        setError("");
        try {
            const response = await addRole(roleArn,finalPermissions);
            setSuccessMsg(response.message+". Redirecting Now");
            console.log(successMsg);
            setTimeout(() => {
                navigate("/dashboard");
              }, 2000);
        }
        catch (error) {
            console.log(error);
            setError(error.response?.data?.detail || "Something went wrong");
        }
        finally {
            setLoading(false);
        }

    };


    return (
        <div>
            <form onSubmit={isPermissionInput ? handlePermissionSubmit : handleRoleSubmit}>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                {isPermissionInput ?
                    <PermissionsHandler
                        selectedActions={selectedActions}
                        toggleAction={toggleAction} />
                    : <RoleHandler
                        launchUrl={launchUrl}
                        roleArn={roleArn}
                        setRoleArn={setRoleArn} />}

                <br></br>
                <button type="submit" disabled={loading}>
                    {isPermissionInput ? "Submit Permissions" : "Submit Role Arn"}
                </button>
                <br></br>
                {successMsg ? <p style={{ color: "green" }}>{successMsg}</p> : null}
                </form>
        </div>
    );
}

export default SetAwsCred;




