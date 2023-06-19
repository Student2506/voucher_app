import React, { useEffect } from 'react';
import './TemplateEditor.scss';
import { useDispatch, useSelector } from "react-redux";
import { getTemplates } from "../../utils/store/templatesSlice";

const TemplateEditor = () => {

  const dispatch = useDispatch();

  useEffect(() => {
    if (templates.length === 0) {
      dispatch(getTemplates());
    }
  }, [])

  const {templates} = useSelector(state => state.templates);

  return (
    <div className={"editor"}>
          <div className={"editor__grid"}>
            {
              templates.map(elem =>
                <div key={elem.id} className={"editor__tile"}><h3 className={"editor__tile_title"}>{elem.title}</h3></div>
              )
            }
          </div>
    </div>
  );
};

export default TemplateEditor;
