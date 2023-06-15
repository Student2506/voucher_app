import React, { useEffect } from 'react';
import './TemplateEditor.scss';
import OptionsMenu from "../OptionsMenu/OptionsMenu";
import { NavLink, Route, Switch } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { getTemplates } from "../../utils/store/templatesSlice";

const TemplateEditor = () => {

  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(getTemplates());
  }, [])

  const {templates} = useSelector(state => state.templates);

  return (
    <div className={"editor"}>
      <OptionsMenu>
        <NavLink exact to={"/template"} className={"menu__link"} activeClassName={"menu__link_active"}>Обзор</NavLink>
        <NavLink to={"/template/create"} className={"menu__link"} activeClassName={"menu__link_active"}>Создать новый шаблон</NavLink>
      </OptionsMenu>
      <Switch>
        <Route exact path={"/template"}>
          <div className={"editor__grid"}>
            {
              templates.map(elem =>
                <div key={elem.id} className={"editor__tile"}><h3 className={"editor__tile_title"}>{elem.title}</h3></div>
              )
            }
          {/*  <div className={"editor__tile"}>*/}
          {/*    <h3 className={"editor__tile_title"}>Base Template 20230320 Сеть кинотеатров</h3>*/}
          {/*  </div>*/}
          {/*  <div className={"editor__tile"}>*/}
          {/*    <h3 className={"editor__tile_title"}>Base Template 20230320 Сеть кинотеатров</h3>*/}
          {/*  </div>*/}
          {/*  <div className={"editor__tile"}>*/}
          {/*    <h3 className={"editor__tile_title"}>Base Template 20230320 Сеть кинотеатровBase Template 20230320 Сеть кинотеатров</h3>*/}
          {/*  </div>*/}
          {/*  <div className={"editor__tile"}>*/}
          {/*    <h3 className={"editor__tile_title"}>Привет, пупс</h3>*/}
          {/*  </div>*/}
          {/*  <div className={"editor__tile"}>*/}
          {/*    <h3 className={"editor__tile_title"}>Привет, пупс</h3>*/}
          {/*  </div>*/}
          {/*  <div className={"editor__tile"}>*/}
          {/*    <h3 className={"editor__tile_title"}>Привет, пупс</h3>*/}
          {/*  </div>*/}
          </div>
        </Route>
        <Route path={"/template/create"}>
          <p>ОЛПАЫФВОРРВЛОЫФРДЫФР</p>
        </Route>
      </Switch>
      {/*<div className={"editor__template"}></div>*/}
      {/*<aside className={"editor__sidebar sidebar"}></aside>*/}
    </div>
  );
};

export default TemplateEditor;
