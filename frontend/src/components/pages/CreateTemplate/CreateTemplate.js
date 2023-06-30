import React from 'react';
import TemplateGrid from "../../TemplateGrid/TemplateGrid";
import './CreateTemplate.scss';
import OptionsMenu from "../../OptionsMenu/OptionsMenu";
import { NavLink, Route, Switch } from "react-router-dom";
import NotFound from "../../NotFound/NotFound";
import { useSelector } from "react-redux";
import LoadingScreen from "../../LoadingScreen/LoadingScreen";
import TemplateEditor from "../../TemplateEditor/TemplateEditor";

const CreateTemplate = () => {

  const {status} = useSelector(state => state.templates);


  return (
    <section className={"create-template"}>
      <OptionsMenu>
        <NavLink exact to={"/template"} className={"menu__link"} activeClassName={"menu__link_active"}>Обзор</NavLink>
        <NavLink to={"/template/create"} className={"menu__link"} activeClassName={"menu__link_active"}>Создать новый шаблон</NavLink>
      </OptionsMenu>
      <Switch>
        <Route exact path={"/template"}>
          <TemplateGrid />
        </Route>
        <Route path={'/template/create'}>
          <NotFound text={"Скоро здесь появиться новая функциональность :)"}/>
          {/*<TemplateEditor />*/}
        </Route>
      </Switch>
      {
        status === 'loading' && <LoadingScreen />
      }
    </section>
  );
};

export default CreateTemplate;
