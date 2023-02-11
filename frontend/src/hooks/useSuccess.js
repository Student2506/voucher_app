import React, { useCallback } from "react";

export default function useSuccess() {
  const [success, setSuccess] = React.useState({});

  const handleSwitchSuccess = useCallback((name, isError) => {
    setSuccess({ ...success, [name]: isError });
  })

  const handleClearErrors = useCallback(() => {
    setSuccess({});
  })

  return { success, handleSwitchSuccess, handleClearErrors };
}
