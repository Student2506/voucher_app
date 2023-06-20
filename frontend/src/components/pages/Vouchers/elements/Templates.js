import React, { useMemo } from 'react';
import ListItems from "../../../ListItems/ListItems";
import { useSelector } from "react-redux";

const Templates = ({onClickItem, filterQuery}) => {

  const {templates} = useSelector(state => state.orders);

  const filtredTemplates = useMemo(() => templates.filter(template => Object.values(template).map((val) => val)[0].toUpperCase().includes(filterQuery.toUpperCase())), [filterQuery, templates]);

  return (
    <>
      {
        filtredTemplates.map((template, i) =>
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
