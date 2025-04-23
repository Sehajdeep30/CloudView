import React from 'react';
import apiClient from '../../api/api.js';
import awsBasicPolicies from './iam_data.js';

function ActionCheckbox({ actionKey, label, checked, onToggle }) {
    return (
        <label style={{ display: "block", marginLeft: 20 }}>
            <input
                type="checkbox"
                checked={checked}
                onChange={() => onToggle(actionKey)}
            />
            {label}
        </label>
    );
}

export function PermissionsHandler({ selectedActions, toggleAction }) {
    return <>
        {Object.entries(awsBasicPolicies).map(([service, categories]) => (
            <div key={service}>
                <h2>{service.toUpperCase()}</h2>

                {Object.keys(categories).map((category) => {
                    const key = `${service}.${category}`;
                    return (
                        <ActionCheckbox
                            key={key}
                            actionKey={key}
                            label={category}
                            checked={selectedActions.includes(key)}
                            onToggle={toggleAction}
                        />
                    );
                })}
            </div>
        ))}
    </>;
}

export function RoleHandler({ launchUrl, setRoleArn, roleArn }) {
    return <>
        <a href={launchUrl}>Click Here To Setup IAM Role</a>
        <br></br><br></br>
        <input
            type='text'
            value={roleArn}
            label="Enter Role Arn"
            onChange={(e) => setRoleArn(e.target.value)}
        />
        <br></br><br></br>
    </>
}

// useAwsCredService.js
export function useAwsCredService() {
    const createLaunchUrl = async (policyArns) => {
        const response = await apiClient.post("/aws_cred/launch_url", { policy_arns: policyArns });
        return response.launch_url;

    }
    const addRole = async (roleArn, policyArns) => {
        const response = await apiClient.post("/aws_cred/add_role", { role_arn: roleArn, policy_arns: policyArns });
        return response;
    }
    return { createLaunchUrl, addRole };
}