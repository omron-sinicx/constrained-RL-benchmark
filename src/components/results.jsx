import React from 'react';
import { render } from 'react-dom';

import { marked } from 'marked';
import markedKatex from 'marked-katex-extension';

const renderer = new marked.Renderer();
renderer.table = (header, body) => {
  return `<div class="uk-overflow-auto"><table class="uk-table uk-table-small uk-text-small uk-table-divider"> ${header} ${body} </table></div>`;
};

marked.use(markedKatex({ throwOnError: false }));
marked.use({ renderer: renderer });

export default class Results extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return this.props.results ? (
      <div className="uk-section">
        <h2 id="results">Results</h2>
        <img
          src={require('../images/HalfCheetah.png')}
          className="uk-responsive-width"
          alt=""
	  width = '400px'
        />
        <img
          src={require('../images/runtime.png')}
          className="uk-responsive-width"
          alt=""
	  width = '400px'
        />
        {this.props.results.map((result, idx) => {
          return (
            <div
              dangerouslySetInnerHTML={{
                __html: marked.parse(result.text),
              }}
            />
          );
        })}
      </div>
    ) : null;
  }
}
