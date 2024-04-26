import React from 'react';
import { render } from 'react-dom';
import Authors from '../components/authors.jsx';
import { FaGithub, FaYoutube, FaMedium } from 'react-icons/fa6';
import { FaFilePdf } from 'react-icons/fa';

class ResourceBtn extends React.Component {
  constructor(props) {
    super(props);
    this.icons = {
      paper: FaFilePdf,
      code: FaGithub,
      video: FaYoutube,
      blog: FaMedium,
    };
  }
  render() {
    if (!this.props.url) return null;
    const aClass =
      this.props.title == 'paper'
        ? `uk-button uk-button-text`
        : `uk-button uk-button-text uk-margin-medium-left`; // FIXME
    const FaIcon = this.icons[this.props.title];
    return (
      <>
        <a className={aClass} href={this.props.url} target="_blank">
          <FaIcon size="2em" color="#1C5EB8" />
          <span className="uk-margin-small-left uk-margin-small-right uk-text-primary uk-text-bolder">
            {this.props.title}
          </span>
        </a>
      </>
    );
  }
}

export default class Header extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const titleClass = `uk-${
      this.props.title.length > 100 ? 'h2' : 'h1'
    } uk-text-primary`;
    return (
      <div className="uk-cover-container uk-background-secondary">
        <div className="uk-container uk-container-small uk-section">
          <div className="uk-text-center uk-text-bold">
            <p className={titleClass}>{this.props.title}</p>
            <span className="uk-label uk-label-primary uk-text-center uk-margin-bottom">
              {this.props.conference}
            </span>
          </div>
          <Authors
            authors={this.props.authors}
            affiliations={this.props.affiliations}
            meta={this.props.meta}
          />
          <div className="uk-flex uk-flex-center uk-margin-top">
            {Object.keys(this.props.resources).map((key) => (
              <ResourceBtn
                url={this.props.resources[key]}
                title={key}
                key={'header-' + key}
              />
            ))}
          </div>
        </div>
      </div>
    );
  }
}
