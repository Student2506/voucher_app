import React from 'react';
import ListItems from "../../../ListItems/ListItems";
import { useSelector } from "react-redux";

const Templates = ({onClickItem}) => {

  const {templates} = useSelector(state => state.orders);

  return (
    <>
      {
        templates.map((template, i) =>
          <ListItems
            listName={"templates"}
            key={i}
            uniqueKey={i}
            title={Object.values(template).map((val) => val)}
            value={Object.keys(template).map((key) => key)}
            onClickItem={onClickItem}
          />
        )
      }
    </>
  );
};

export default Templates;
