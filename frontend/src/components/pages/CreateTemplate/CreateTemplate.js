import React, { useCallback, useState } from 'react';
import TemplateGrid from "../../TemplateGrid/TemplateGrid";
import './CreateTemplate.scss';
import OptionsMenu from "../../OptionsMenu/OptionsMenu";
import { NavLink, Route, Switch, useHistory } from "react-router-dom";
import NotFound from "../../NotFound/NotFound";
import { useDispatch, useSelector } from "react-redux";
import LoadingScreen from "../../LoadingScreen/LoadingScreen";
import TemplateEditor from "../../TemplateEditor/TemplateEditor";
import { updateTemplate } from "../../../utils/store/templatesSlice";

const CreateTemplate = () => {

  const {status} = useSelector(state => state.templates);

  const [updatedTemplate, setUpdatedTemplate] = useState({});
  const [selectedTemplate, setSelectedTemplate] = useState({});
  const history = useHistory();
  const dispatch = useDispatch();
  function editTemplateProperty(template) {
    template.template_property.forEach(property => {
      const content = property.content;
      const regex = /<[^>]*>(.*?)<\/[^>]*>/g;
      const matches = Array.from(content.matchAll(regex), match => match[1].replace(/<\/?[^>]+(>|$)/g, ''));
      property.editedContent = matches
    })
    return template;
  }

  const onChoiceTemplate = useCallback((template) => {
    setSelectedTemplate(editTemplateProperty(template));
    history.push('/template/create')
  }, [])

  // function updateTemplateContent(template) {
  //   const updatedTemplate = { ...template };
  //
  //   updatedTemplate.template_property.forEach((property) => {
  //     if (property.editedContent && property.editedContent.length > 0) {
  //       const updatedContent = property.content.replace(/>(.*?)</g, (match, p1) => {
  //         const editedLine = property.editedContent.shift();
  //         return `>${editedLine}<`;
  //       });
  //
  //       property.content = updatedContent;
  //     }
  //   });
  //
  //   dispatch(updateTemplate(updatedTemplate))
  //   // setUpdatedTemplate(updatedTemplate);
  // }

  return (
    <section className={"create-template"}>
      <OptionsMenu>
        <NavLink exact to={"/template"} className={"menu__link"} activeClassName={"menu__link_active"}>Обзор</NavLink>
        <NavLink to={"/template/create"} className={"menu__link"} activeClassName={"menu__link_active"}>Создать новый шаблон</NavLink>
      </OptionsMenu>
      <Switch>
        <Route exact path={"/template"}>
          <TemplateGrid onCLick={onChoiceTemplate} />
        </Route>
        <Route path={'/template/create'}>
          {/*<NotFound text={"Скоро здесь появиться новая функциональность :)"}/>*/}
          <TemplateEditor template={selectedTemplate} />
        </Route>
      </Switch>
      {
        status === 'loading' && <LoadingScreen />
      }
    </section>
  );
};

export default React.memo(CreateTemplate);
