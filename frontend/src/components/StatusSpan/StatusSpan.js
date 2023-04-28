import React from 'react';
import styles from '../../styles/statusSpan.scss';

const StatusSpan = ({status, rejectedMessage, resolvedMessage}) => {
  return (
    <span className={`status-span ${status === 'resolved' ? "status-span__res" : status === 'rejected' ? "status-span__rej" : ""}`}>
      {status === 'resolved' ? resolvedMessage : status === 'rejected' ? rejectedMessage : " "}
    </span>
  );
};

export default StatusSpan;
