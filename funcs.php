<?php

/**
 *
 *
 *
 * Based on http://stackoverflow.com/questions/5868480/how-should-i-get-a-divs-content-like-this-using-dom-in-php
 **/

function DOMinnerText($element)
{
    $innerHTML = "";
    $children = $element->childNodes;
    foreach ($children as $child)
    {
        $tmp_dom = new DOMDocument();
        $tmp_dom->appendChild($tmp_dom->importNode($child, true));
        $innerHTML.=trim($tmp_dom->saveHTML());
    }
    return html_entity_decode($innerHTML);
}


