import React from 'react';
import { render } from 'react-dom';

export default class Citation extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="uk-section">
        <h2>Citation</h2>
        <pre>
          <code>{this.props.bibtex}</code>
        </pre>
      </div>
    );
  }
}
