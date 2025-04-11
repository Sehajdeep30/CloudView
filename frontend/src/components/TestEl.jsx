function TestEl() {
    console.log("inside test");
    
    const handleSubmit = () => {
        logout();
        navigate("/login");
    }

    return (<>
        <h1>Welcome to the tester</h1>
        <a href="/dashboard">go to dashboard</a>
    </>);
}

export default TestEl;