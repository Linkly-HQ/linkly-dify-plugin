# Privacy Policy - Linkly plugin for Dify

Last updated: 13 September 2026

## Who operates this plugin

This plugin is published by Linkly Ltd (United Kingdom, company no. 15327126), the operator of the Linkly URL shortener at https://linklyhq.com. Contact: support@linklyhq.com.

## What the plugin does with your data

The plugin is a thin client for the Linkly REST API (`https://api.linklyhq.com`). Every tool call sends the parameters you (or the model) supply - destination URLs, link names, slugs, UTM tags, link IDs, date ranges and filters - together with your Linkly API key, over HTTPS to the Linkly API, and returns the API response to your Dify workflow.

## Credentials

Your Linkly API key and optional workspace ID are entered in the Dify provider settings and stored by your Dify instance using Dify's credential storage. The plugin reads them only at call time and sends them only to `api.linklyhq.com` as a Bearer token. The plugin never logs, caches or forwards credentials anywhere else.

## Data collected by the plugin itself

None. The plugin keeps no state, database, cache or log of its own. Nothing is sent to any third party other than the Linkly API.

## Data held by Linkly

Links you create, and the click events recorded when someone opens them, are stored in your Linkly workspace under the Linkly privacy policy: https://linklyhq.com/support/privacy. You can delete links from the Linkly app or with this plugin's `delete_link` tool, and delete your account at any time.

## Personal data

Click analytics returned by the analytics tools may include the country, city, platform, browser and referrer of people who clicked your links, as recorded by Linkly. IP addresses are not returned by the tools in this plugin.

## Questions

Email support@linklyhq.com.
