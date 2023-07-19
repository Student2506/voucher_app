import React, { useEffect, useState } from 'react';
import logoVoucher from '../../images/logoVoucher.png';
import shtrih from '../../images/shtrih.png';
import titleImage from '../../images/voucher.png';
import { MAX_TEXTAREA_COUNT } from "../../constants";
import './TemplateEditor.scss';
import StatusSpan from "../StatusSpan/StatusSpan";
import { useDispatch, useSelector } from "react-redux";
import { dropStatus, updateTemplate } from "../../utils/store/templatesSlice";

const TemplateEditor = ({template}) => {

  const [cl, setCl] = useState(0);

  const values = {
    subtitle: template.template_property.find(elem => elem.name === 'refactor_subtitle'),
    conditions: template.template_property.find(elem => elem.name === 'refactor_conditions'),
    caption: template.template_property.find(elem => elem.name === 'refactor_caption'),
    bottomCaption: template.template_property.find(elem => elem.name === 'refactor_bottom_caption'),
    text: template.template_property.find(elem => elem.name === "voucher_text"),
    bottom: template.template_property.find(elem => elem.name === 'refactor_bottom'),
  }

  function restoreTemplateFromValues() {
    submitEditTemplate();
    // Создаем копию исходного объекта template
    const restoredTemplate =  JSON.parse(JSON.stringify(template));

    // Восстанавливаем измененные значения из объекта values
    restoredTemplate.template_property.forEach(elem => {
      if (values[elem.name]) {
        const foundValue = values[elem.name];
        const editedContent = foundValue.editedContent;

        if (editedContent && Array.isArray(editedContent)) {
          editedContent.forEach((value, index) => {
            if (elem.content && Array.isArray(elem.content)) {
              elem.content[index].text = value;
            }
          });
        }
      }
    });

    const updatedTemplate = { ...restoredTemplate };

    updatedTemplate.template_property.forEach((property) => {
      if (property.editedContent && property.editedContent.length > 0) {
        const updatedContent = property.content.replace(/>(.*?)</g, (match, p1) => {
          const editedLine = property.editedContent.shift();
          return `>${editedLine}<`;
        });

        property.content = updatedContent;
      }
    });

    return updatedTemplate;
  }

  const dispatch = useDispatch();
  const [selectedText, setSelectedText] = useState({block: '', elemNumber: '', currentValue: ''});
  const {status} = useSelector(state => state.templates);

  function selectText(e, block, elemNumber) {
    setSelectedText({block, elemNumber, currentValue: e.target.innerHTML});
  }

  function decodeHTMLEntities(text) {
    const textArea = document.createElement('textarea');
    textArea.innerHTML = text;
    return textArea.value;
  }

  function submitEditTemplate() {
    values[selectedText.block].editedContent[selectedText.elemNumber] = selectedText.currentValue;
  }

  useEffect(() => {
    if(selectedText.currentValue !== '' && cl > 0) {
      dispatch(updateTemplate(restoreTemplateFromValues()));
    }
  }, [cl])

  // dispatch(dropStatus());
  return (
    <div className={"templateEditor"}>
      <div className={"template"}>
        <article className={"template__header template__border"}>
          <div className={"template__logo"} />
          <h2 className={"template__title template__clickable"} onClick={(e) => {selectText(e, 'subtitle', 0)}}>{decodeHTMLEntities(values.subtitle.editedContent[0])}</h2>
          <h2 className={"template__title template__clickable"} onClick={(e) => {selectText(e, 'subtitle', 1)}}>{decodeHTMLEntities(values.subtitle.editedContent[1])}</h2>
          <h3 className={"template__subtitle"}>*Подробнисти у администратора кинотеатра</h3>
        </article>
        <article className={"template__main template__border"}>
            <img className={"template__shtrih"} src={shtrih}/>
            <img className={"template__voucher-image"} src={titleImage}/>
        </article>
        <article className={"template__footer"}>
          <h3 className={"template__subtitle template__subtitle_black template__clickable"} onClick={(e) => {selectText(e, 'bottomCaption', 0)}}>
            {decodeHTMLEntities(values.bottomCaption.editedContent[0])}
          </h3>
          <h3 className={"template__subtitle template__subtitle_black template__clickable"} onClick={(e) => {selectText(e, 'bottomCaption', 1)}}>
            {decodeHTMLEntities(values.bottomCaption.editedContent[1])}
          </h3>
          <ol className={"template__texts"}>
            {
              values.text.editedContent.map((text, i) =>
              <li className={"template__text template__clickable"} key={i} value={i+1} onClick={(e) => {selectText(e, "text", i)}}>
                {decodeHTMLEntities(text)}
              </li>
              )
            }
          </ol>
        </article>
      </div>
      {selectedText !== '' && <aside className={"template__sidebar"}>
        <textarea className={"template__textarea"} value={selectedText.currentValue}
                  onChange={(e) => {setSelectedText({...selectedText, currentValue: e.target.value})}}></textarea>
        <div className={"template__button-section"}>
          <StatusSpan status={status} rejectedMessage={"Упс, что-то пошло не так..."} resolvedMessage={"Сертификат успешно обновлен"}/>
          <button type={"button"} className={"button button_theme_blue"} onClick={() => {setCl(cl + 1)}}>Сохранить</button>
        </div>
      </aside>}
    </div>
  );
};

export default TemplateEditor;
