/**
 * Rural Literacy AI Tool - Mobile App
 * A React Native application for rural literacy education
 * Version 2.0 - Enhanced UI
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  SafeAreaView,
  StatusBar,
  FlatList,
  Alert,
  AsyncStorage,
  Image,
  KeyboardAvoidingView,
  Platform
} from 'react-native';

// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// Color Palette
const COLORS = {
  primary: '#6366F1',
  primaryDark: '#4F46E5',
  primaryLight: '#A5B4FC',
  secondary: '#10B981',
  secondaryDark: '#059669',
  accent: '#F59E0B',
  danger: '#EF4444',
  background: '#F3F4F6',
  surface: '#FFFFFF',
  surfaceSecondary: '#F9FAFB',
  text: '#111827',
  textSecondary: '#6B7280',
  textLight: '#9CA3AF',
  border: '#E5E7EB',
  userBubble: '#6366F1',
  botBubble: '#FFFFFF',
  shadow: '#000000'
};

// Main App Component
export default function App() {
  const [currentScreen, setCurrentScreen] = useState('home');
  const [userId, setUserId] = useState('');
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isOnline, setIsOnline] = useState(true);
  const [chatMode, setChatMode] = useState('auto');
  const [syncStatus, setSyncStatus] = useState({ pending: 0, syncing: false });
  const flatListRef = useRef(null);

  useEffect(() => {
    checkConnectivity();
    loadUser();
  }, []);

  useEffect(() => {
    // Scroll to bottom when new message arrives
    if (messages.length > 0 && flatListRef.current) {
      setTimeout(() => {
        flatListRef.current?.scrollToEnd({ animated: true });
      }, 100);
    }
  }, [messages]);

  const checkConnectivity = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/`);
      const data = await response.json();
      setIsOnline(data.connectivity);
    } catch (error) {
      setIsOnline(false);
    }
  };

  const loadUser = async () => {
    try {
      const savedUserId = await AsyncStorage.getItem('userId');
      if (savedUserId) {
        setUserId(savedUserId);
        loadChatHistory(savedUserId);
      } else {
        const newUserId = `user_${Date.now()}`;
        await AsyncStorage.setItem('userId', newUserId);
        setUserId(newUserId);
      }
    } catch (error) {
      console.error('Error loading user:', error);
    }
  };

  const loadChatHistory = async (uid) => {
    try {
      const response = await fetch(`${API_BASE_URL}/history/${uid}`);
      const history = await response.json();
      if (Array.isArray(history) && history.length > 0) {
        const formattedMessages = history.reverse().map(chat => ({
          id: chat.id.toString(),
          userMessage: chat.message,
          botMessage: chat.response,
          mode: chat.mode,
          timestamp: chat.timestamp
        }));
        setMessages(formattedMessages);
      }
    } catch (error) {
      console.error('Error loading chat history:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || !userId) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setIsLoading(true);

    const tempId = Date.now().toString();
    setMessages(prev => [...prev, {
      id: tempId,
      userMessage: userMessage,
      botMessage: '',
      mode: 'sending',
      timestamp: new Date().toISOString(),
      isLoading: true
    }]);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          user_id: userId,
          mode: chatMode
        })
      });

      const data = await response.json();

      if (response.ok) {
        setMessages(prev => prev.map(msg => 
          msg.id === tempId 
            ? { ...msg, botMessage: data.response, mode: data.mode, isLoading: false }
            : msg
        ));
        setSyncStatus(prev => ({ ...prev, pending: prev.pending + 1 }));
      } else {
        Alert.alert('Error', data.detail || 'Failed to get response');
        setMessages(prev => prev.filter(msg => msg.id !== tempId));
      }
    } catch (error) {
      Alert.alert('Connection Error', 'Unable to connect to server. Please check your connection.');
      setMessages(prev => prev.filter(msg => msg.id !== tempId));
    } finally {
      setIsLoading(false);
    }
  };

  const syncData = async () => {
    setSyncStatus(prev => ({ ...prev, syncing: true }));
    try {
      const response = await fetch(`${API_BASE_URL}/sync`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ force_sync: false })
      });
      const data = await response.json();
      
      if (data.success) {
        setSyncStatus({ pending: 0, syncing: false });
        Alert.alert('✅ Sync Complete', data.message);
      } else {
        setSyncStatus(prev => ({ ...prev, syncing: false }));
        Alert.alert('⚠️ Sync Status', data.message);
      }
    } catch (error) {
      setSyncStatus(prev => ({ ...prev, syncing: false }));
      Alert.alert('Sync Error', 'Failed to sync data');
    }
  };

  const clearChat = () => {
    Alert.alert(
      'Clear Chat',
      'Are you sure you want to clear all messages?',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Clear', 
          style: 'destructive',
          onPress: () => setMessages([])
        }
      ]
    );
  };

  const getModeColor = (mode) => {
    switch(mode) {
      case 'online': return COLORS.secondary;
      case 'offline': return COLORS.accent;
      default: return COLORS.primary;
    }
  };

  const getModeIcon = (mode) => {
    switch(mode) {
      case 'online': return '🌐';
      case 'offline': return '💾';
      default: return '🤖';
    }
  };

  const renderMessage = ({ item, index }) => (
    <View style={styles.messageWrapper}>
      {/* User Message */}
      <View style={styles.messageRow}>
        <View style={styles.messageSpacer} />
        <View style={styles.userMessageBubble}>
          <Text style={styles.messageText}>{item.userMessage}</Text>
          <Text style={styles.messageTime}>
            {new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </Text>
        </View>
      </View>

      {/* Bot Message */}
      {(item.botMessage || item.isLoading) && (
        <View style={styles.botMessageRow}>
          <View style={styles.botAvatar}>
            <Text style={styles.botAvatarText}>AI</Text>
          </View>
          <View style={styles.botMessageBubble}>
            {item.isLoading ? (
              <View style={styles.loadingContainer}>
                <ActivityIndicator size="small" color={COLORS.primary} />
                <Text style={styles.loadingText}>Thinking...</Text>
              </View>
            ) : (
              <>
                <Text style={styles.botMessageText}>{item.botMessage}</Text>
                <View style={styles.botMessageFooter}>
                  <Text style={[styles.modeTag, { backgroundColor: getModeColor(item.mode) + '20' }]}>
                    {getModeIcon(item.mode)} {item.mode}
                  </Text>
                  <Text style={styles.messageTime}>
                    {new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </Text>
                </View>
              </>
            )}
          </View>
        </View>
      )}
    </View>
  );

  const HomeScreen = () => (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor={COLORS.background} />
      
      {/* Header */}
      <View style={styles.homeHeader}>
        <View style={styles.logoContainer}>
          <View style={styles.logo}>
            <Text style={styles.logoText}>📚</Text>
          </View>
          <View>
            <Text style={styles.appTitle}>Rural Literacy</Text>
            <Text style={styles.appSubtitle}>AI Tool</Text>
          </View>
        </View>
        <View style={[styles.connectionBadge, isOnline ? styles.onlineBadge : styles.offlineBadge]}>
          <Text style={styles.connectionIcon}>{isOnline ? '🟢' : '🟠'}</Text>
          <Text style={styles.connectionText}>{isOnline ? 'Online' : 'Offline'}</Text>
        </View>
      </View>

      {/* Stats Card */}
      <View style={styles.statsCard}>
        <View style={styles.statItem}>
          <Text style={styles.statNumber}>{messages.length}</Text>
          <Text style={styles.statLabel}>Messages</Text>
        </View>
        <View style={styles.statDivider} />
        <View style={styles.statItem}>
          <Text style={styles.statNumber}>{syncStatus.pending}</Text>
          <Text style={styles.statLabel}>Pending Sync</Text>
        </View>
        <View style={styles.statDivider} />
        <View style={styles.statItem}>
          <Text style={styles.statNumber}>{userId.slice(-4)}</Text>
          <Text style={styles.statLabel}>Session</Text>
        </View>
      </View>

      {/* Main Menu */}
      <View style={styles.menuContainer}>
        <TouchableOpacity 
          style={styles.mainButton} 
          onPress={() => setCurrentScreen('chat')}
          activeOpacity={0.8}
        >
          <View style={styles.mainButtonContent}>
            <View style={styles.mainButtonIcon}>
              <Text style={styles.mainButtonEmoji}>💬</Text>
            </View>
            <View style={styles.mainButtonTextContainer}>
              <Text style={styles.mainButtonTitle}>Start Chat</Text>
              <Text style={styles.mainButtonSubtitle}>Ask questions, learn new things</Text>
            </View>
          </View>
          <Text style={styles.mainButtonArrow}>→</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.mainButton, syncStatus.syncing && styles.mainButtonDisabled]} 
          onPress={syncData}
          disabled={syncStatus.syncing}
          activeOpacity={0.8}
        >
          <View style={styles.mainButtonContent}>
            <View style={[styles.mainButtonIcon, { backgroundColor: COLORS.secondary + '20' }]}>
              <Text style={styles.mainButtonEmoji}>🔄</Text>
            </View>
            <View style={styles.mainButtonTextContainer}>
              <Text style={styles.mainButtonTitle}>Sync Data</Text>
              <Text style={styles.mainButtonSubtitle}>
                {syncStatus.syncing ? 'Syncing...' : `${syncStatus.pending} items pending`}
              </Text>
            </View>
          </View>
          {syncStatus.syncing && <ActivityIndicator size="small" color={COLORS.secondary} />}
        </TouchableOpacity>

        <TouchableOpacity 
          style={styles.mainButton} 
          onPress={checkConnectivity}
          activeOpacity={0.8}
        >
          <View style={styles.mainButtonContent}>
            <View style={[styles.mainButtonIcon, { backgroundColor: COLORS.accent + '20' }]}>
              <Text style={styles.mainButtonEmoji}>🔗</Text>
            </View>
            <View style={styles.mainButtonTextContainer}>
              <Text style={styles.mainButtonTitle}>Check Connection</Text>
              <Text style={styles.mainButtonSubtitle}>Test your network status</Text>
            </View>
          </View>
          <Text style={styles.mainButtonArrow}>→</Text>
        </TouchableOpacity>
      </View>

      {/* Mode Selector Card */}
      <View style={styles.modeCard}>
        <Text style={styles.modeCardTitle}>AI Mode</Text>
        <View style={styles.modeSelector}>
          {['auto', 'online', 'offline'].map((mode) => (
            <TouchableOpacity
              key={mode}
              style={[
                styles.modeChip,
                chatMode === mode && styles.modeChipActive,
                { borderColor: chatMode === mode ? getModeColor(mode) : COLORS.border }
              ]}
              onPress={() => setChatMode(mode)}
            >
              <Text style={styles.modeChipIcon}>{getModeIcon(mode)}</Text>
              <Text style={[
                styles.modeChipText,
                chatMode === mode && { color: getModeColor(mode) }
              ]}>
                {mode.charAt(0).toUpperCase() + mode.slice(1)}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      {/* Footer */}
      <View style={styles.footer}>
        <Text style={styles.footerText}>Version 1.0.0 • Rural Literacy AI</Text>
      </View>
    </SafeAreaView>
  );

  const ChatScreen = () => (
    <SafeAreaView style={styles.chatContainer}>
      <StatusBar barStyle="dark-content" backgroundColor={COLORS.surface} />
      
      {/* Chat Header */}
      <View style={styles.chatHeader}>
        <TouchableOpacity 
          style={styles.backButton} 
          onPress={() => setCurrentScreen('home')}
        >
          <Text style={styles.backButtonText}>←</Text>
        </TouchableOpacity>
        
        <View style={styles.chatHeaderCenter}>
          <Text style={styles.chatHeaderTitle}>AI Assistant</Text>
          <View style={styles.chatHeaderStatus}>
            <View style={[styles.statusDot, { backgroundColor: isOnline ? COLORS.secondary : COLORS.accent }]} />
            <Text style={styles.chatHeaderSubtitle}>
              {isOnline ? 'Connected' : 'Offline Mode'}
            </Text>
          </View>
        </View>

        <TouchableOpacity style={styles.headerAction} onPress={clearChat}>
          <Text style={styles.headerActionText}>🗑️</Text>
        </TouchableOpacity>
      </View>

      {/* Mode Indicator */}
      <View style={styles.chatModeBar}>
        <Text style={styles.chatModeLabel}>Current Mode:</Text>
        <View style={[styles.chatModeBadge, { backgroundColor: getModeColor(chatMode) }]}>
          <Text style={styles.chatModeText}>{getModeIcon(chatMode)} {chatMode.toUpperCase()}</Text>
        </View>
      </View>

      {/* Messages */}
      <FlatList
        ref={flatListRef}
        data={messages}
        renderItem={renderMessage}
        keyExtractor={item => item.id}
        style={styles.messageList}
        contentContainerStyle={styles.messageListContent}
        showsVerticalScrollIndicator={false}
        ListEmptyComponent={
          <View style={styles.emptyState}>
            <Text style={styles.emptyStateIcon}>💭</Text>
            <Text style={styles.emptyStateTitle}>No messages yet</Text>
            <Text style={styles.emptyStateSubtitle}>Start a conversation with the AI</Text>
          </View>
        }
      />

      {/* Input Area */}
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
      >
        <View style={styles.inputContainer}>
          <View style={styles.inputWrapper}>
            <TextInput
              style={styles.input}
              value={inputMessage}
              onChangeText={setInputMessage}
              placeholder="Type your message..."
              placeholderTextColor={COLORS.textLight}
              multiline
              maxLength={1000}
            />
            <Text style={styles.charCount}>{inputMessage.length}/1000</Text>
          </View>
          
          <TouchableOpacity 
            style={[
              styles.sendButton,
              (!inputMessage.trim() || isLoading) && styles.sendButtonDisabled
            ]}
            onPress={sendMessage}
            disabled={!inputMessage.trim() || isLoading}
          >
            {isLoading ? (
              <ActivityIndicator size="small" color="#fff" />
            ) : (
              <Text style={styles.sendButtonText}>➤</Text>
            )}
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );

  return currentScreen === 'home' ? <HomeScreen /> : <ChatScreen />;
}

const styles = StyleSheet.create({
  // Container Styles
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  chatContainer: {
    flex: 1,
    backgroundColor: COLORS.background,
  },

  // Home Screen Styles
  homeHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 15,
    backgroundColor: COLORS.surface,
  },
  logoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  logo: {
    width: 50,
    height: 50,
    borderRadius: 15,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  logoText: {
    fontSize: 24,
  },
  appTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  appSubtitle: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  connectionBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    backgroundColor: COLORS.surfaceSecondary,
  },
  onlineBadge: {
    backgroundColor: COLORS.secondary + '15',
  },
  offlineBadge: {
    backgroundColor: COLORS.accent + '15',
  },
  connectionIcon: {
    fontSize: 10,
    marginRight: 6,
  },
  connectionText: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.text,
  },

  // Stats Card
  statsCard: {
    flexDirection: 'row',
    marginHorizontal: 20,
    marginTop: 15,
    padding: 15,
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    shadowColor: COLORS.shadow,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 10,
    elevation: 3,
  },
  statItem: {
    flex: 1,
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.primary,
  },
  statLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  statDivider: {
    width: 1,
    backgroundColor: COLORS.border,
    marginVertical: 5,
  },

  // Menu Styles
  menuContainer: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 20,
  },
  mainButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: COLORS.surface,
    padding: 16,
    borderRadius: 16,
    marginBottom: 12,
    shadowColor: COLORS.shadow,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 10,
    elevation: 3,
  },
  mainButtonDisabled: {
    opacity: 0.7,
  },
  mainButtonContent: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  mainButtonIcon: {
    width: 48,
    height: 48,
    borderRadius: 14,
    backgroundColor: COLORS.primary + '15',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 14,
  },
  mainButtonEmoji: {
    fontSize: 22,
  },
  mainButtonTextContainer: {
    flex: 1,
  },
  mainButtonTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
  },
  mainButtonSubtitle: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  mainButtonArrow: {
    fontSize: 20,
    color: COLORS.textLight,
  },

  // Mode Card
  modeCard: {
    marginHorizontal: 20,
    marginBottom: 20,
    padding: 16,
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    shadowColor: COLORS.shadow,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 10,
    elevation: 3,
  },
  modeCardTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.textSecondary,
    marginBottom: 12,
  },
  modeSelector: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  modeChip: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 10,
    marginHorizontal: 4,
    borderRadius: 12,
    borderWidth: 1.5,
    backgroundColor: COLORS.surfaceSecondary,
  },
  modeChipActive: {
    backgroundColor: COLORS.surface,
  },
  modeChipIcon: {
    fontSize: 14,
    marginRight: 6,
  },
  modeChipText: {
    fontSize: 13,
    fontWeight: '600',
    color: COLORS.textSecondary,
  },

  // Footer
  footer: {
    padding: 15,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 12,
    color: COLORS.textLight,
  },

  // Chat Screen Styles
  chatHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 15,
    paddingVertical: 12,
    backgroundColor: COLORS.surface,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  backButton: {
    padding: 8,
  },
  backButtonText: {
    fontSize: 24,
    color: COLORS.primary,
  },
  chatHeaderCenter: {
    flex: 1,
    alignItems: 'center',
  },
  chatHeaderTitle: {
    fontSize: 17,
    fontWeight: '600',
    color: COLORS.text,
  },
  chatHeaderStatus: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 2,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 6,
  },
  chatHeaderSubtitle: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
  headerAction: {
    padding: 8,
  },
  headerActionText: {
    fontSize: 20,
  },

  chatModeBar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 8,
    backgroundColor: COLORS.surfaceSecondary,
  },
  chatModeLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginRight: 8,
  },
  chatModeBadge: {
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  chatModeText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#fff',
  },

  // Message Styles
  messageList: {
    flex: 1,
  },
  messageListContent: {
    padding: 15,
    paddingBottom: 20,
  },
  messageWrapper: {
    marginBottom: 15,
  },
  messageRow: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    justifyContent: 'flex-end',
  },
  messageSpacer: {
    flex: 1,
  },
  userMessageBubble: {
    backgroundColor: COLORS.userBubble,
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    borderBottomLeftRadius: 20,
    borderBottomRightRadius: 4,
    maxWidth: '85%',
    shadowColor: COLORS.primary,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 2,
  },
  messageText: {
    fontSize: 15,
    color: '#fff',
    lineHeight: 21,
  },
  messageTime: {
    fontSize: 10,
    color: 'rgba(255,255,255,0.7)',
    marginTop: 4,
    alignSelf: 'flex-end',
  },

  botMessageRow: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    marginTop: 10,
  },
  botAvatar: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 10,
  },
  botAvatarText: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#fff',
  },
  botMessageBubble: {
    backgroundColor: COLORS.botBubble,
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    borderBottomLeftRadius: 4,
    borderBottomRightRadius: 20,
    maxWidth: '75%',
    shadowColor: COLORS.shadow,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  botMessageText: {
    fontSize: 15,
    color: COLORS.text,
    lineHeight: 21,
  },
  botMessageFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginTop: 6,
  },
  modeTag: {
    fontSize: 10,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 8,
    overflow: 'hidden',
  },

  // Loading State
  loadingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginLeft: 8,
  },

  // Empty State
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 100,
  },
  emptyStateIcon: {
    fontSize: 60,
    marginBottom: 15,
  },
  emptyStateTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 8,
  },
  emptyStateSubtitle: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },

  // Input Styles
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    padding: 12,
    backgroundColor: COLORS.surface,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
  },
  inputWrapper: {
    flex: 1,
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    marginRight: 10,
    maxHeight: 100,
  },
  input: {
    fontSize: 15,
    color: COLORS.text,
    maxHeight: 80,
    padding: 0,
  },
  charCount: {
    fontSize: 10,
    color: COLORS.textLight,
    textAlign: 'right',
    marginTop: 4,
  },
  sendButton: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: COLORS.primary,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 3,
  },
  sendButtonDisabled: {
    backgroundColor: COLORS.textLight,
    shadowOpacity: 0,
  },
  sendButtonText: {
    fontSize: 20,
    color: '#fff',
  },
});
