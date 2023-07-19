import React, { useEffect } from 'react';
import './TemplateGrid.scss';
import { useDispatch, useSelector } from "react-redux";
import { getTemplates } from "../../utils/store/templatesSlice";

const TemplateGrid = ({onCLick}) => {

  const dispatch = useDispatch();

  useEffect(() => {
    if (templates.length === 0) {
      dispatch(getTemplates());
    }
  }, [])

  const {templates} = useSelector(state => state.templates);

  function onClickTemplate(id) {
    const selectedTemplate = JSON.parse(JSON.stringify(templates.find(template => template.id === id)));
    onCLick(selectedTemplate);
  }

  return (
    <div className={"editor"}>
          <div className={"editor__grid"}>
            {
              templates.map(elem =>
                <div onClick={() => {onClickTemplate(elem.id)}} key={elem.id} className={"editor__tile"}><h3 className={"editor__tile_title"}>{elem.title}</h3></div>
              )
            }
          </div>
    </div>
  );
};

export default TemplateGrid;
