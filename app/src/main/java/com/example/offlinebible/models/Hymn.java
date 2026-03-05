package com.example.offlinebible.models;

import java.util.List;

public class Hymn {
    private int id;
    private int number;
    private String title;
    private List<String> stanzas;

    public Hymn(int id, int number, String title) {
        this.id = id;
        this.number = number;
        this.title = title;
    }

    public int getId() {
        return id;
    }

    public int getNumber() {
        return number;
    }

    public String getTitle() {
        return title;
    }

    public List<String> getStanzas() {
        return stanzas;
    }

    public void setStanzas(List<String> stanzas) {
        this.stanzas = stanzas;
    }
}
