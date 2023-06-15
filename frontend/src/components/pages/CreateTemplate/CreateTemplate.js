import React from 'react';
import TemplateEditor from "../../TemplateEditor/TemplateEditor";
import './CreateTemplate.scss';
import OptionsMenu from "../../OptionsMenu/OptionsMenu";

const CreateTemplate = () => {
  return (
    <section className={"create-template"}>
      <TemplateEditor />
    </section>
  );
};

export default CreateTemplate;
