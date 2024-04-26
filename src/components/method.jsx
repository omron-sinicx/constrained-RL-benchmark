import React from 'react';
import { render } from 'react-dom';
import { marked } from 'marked';
import markedKatex from 'marked-katex-extension';
marked.use(markedKatex({ throwOnError: false }));

class Content extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    if (this.props.title) return <h2>{this.props.title}</h2>;
    if (this.props.text)
      return (
        <div
          dangerouslySetInnerHTML={{ __html: marked.parse(this.props.text) }}
        />
      );
    if (this.props.image)
      return (
        <img
          src={require('../images/alpha.png')}
          className="uk-align-center uk-responsive-width"
          alt=""
        />
      );
    return null;
  }
}

export default class Method extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return this.props.method ? (
      <div className="uk-section">
        {this.props.method.map((subsection, idx) => {
          return (
            <div key={'subsection-' + idx}>
              <Content title={subsection.title} />
        <img
          src={require('../images/closest.png')}
          className="uk-responsive-width"
          alt=""
	  width = '300px'
        />
        <img
          src={require('../images/alpha.png')}
          className="uk-responsive-width"
          alt=""
	  width = '300px'
        />
        <img
          src={require('../images/radial.png')}
          className="uk-responsive-width"
          alt=""
	  width = '300px'
        />
              <Content text={subsection.text} />
            </div>
          );
        })}
      </div>
    ) : null;
  }
}
