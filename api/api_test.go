package api

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"snapshot/msg"
)

func TestIndex(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	w := httptest.NewRecorder()

	handleIndex(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("Invalid status code %d", w.Code)
	}
}

func TestSmsUnverified(t *testing.T) {
	req := httptest.NewRequest(http.MethodPost, "/sms", nil)
	w := httptest.NewRecorder()

	handler := handleSms(msg.NewShellClient())
	handler(w, req)

	if w.Code != http.StatusUnauthorized {
		t.Fatalf("Expected unathorized %d", w.Code)
	}
}
