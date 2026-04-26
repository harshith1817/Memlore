import { useEffect } from "react";

function OAuthSuccess() {

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");

    if (token) {
      localStorage.setItem("token", token);
        window.location.href = "/chat";
    } else {
        window.location.href = "/";
    }
  }, []);

  return <p>Logging you in...</p>;
}

export default OAuthSuccess;