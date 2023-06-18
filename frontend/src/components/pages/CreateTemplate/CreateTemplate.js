import React from 'react';
import TemplateEditor from "../../TemplateEditor/TemplateEditor";
import './CreateTemplate.scss';
import OptionsMenu from "../../OptionsMenu/OptionsMenu";
import { NavLink, Route, Switch } from "react-router-dom";
import NotFound from "../../NotFound/NotFound";
import PagePreloader from "../../PagePreloader/PagePreloader";

const CreateTemplate = () => {
  return (
    <section className={"create-template"}>
      <OptionsMenu>
        <NavLink exact to={"/template"} className={"menu__link"} activeClassName={"menu__link_active"}>Обзор</NavLink>
        <NavLink to={"/template/create"} className={"menu__link"} activeClassName={"menu__link_active"}>Создать новый шаблон</NavLink>
      </OptionsMenu>
      <Switch>
        <Route exact path={"/template"}>
          <TemplateEditor />
        </Route>
        <Route path={'/template/create'}>
          {/*<NotFound text={"Скоро здесь появиться новая функциональность :)"}/>*/}
          {/*<PagePreloader />*/}
        </Route>
      </Switch>
    </section>
  );
};

export default CreateTemplate;
